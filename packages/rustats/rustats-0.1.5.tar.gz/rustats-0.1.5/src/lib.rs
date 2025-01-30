use pyo3::prelude::*;
use pyo3::types::{IntoPyDict, PyAny, PyDict, PyList, PyType};
use pyo3::wrap_pyfunction;

use numpy::{PyArray1, PyArray2, IntoPyArray};
use ndarray::{Array1, Array2, ArrayView1, ArrayView2, s, Axis};
use statrs::distribution::{Continuous, Normal, ContinuousCDF};
use std::collections::HashMap;
use std::fmt::Write as _;  // for building cluster-keys

/// Add significance stars.
fn add_significance_stars(p: f64) -> &'static str {
    if p < 0.01 {
        "***"
    } else if p < 0.05 {
        "**"
    } else if p < 0.1 {
        "*"
    } else {
        ""
    }
}

/// Downcast a Python object to NumPy PyArray2<f64> => ndarray::ArrayView2<f64>.
///
/// Marked unsafe because .as_array() in pyo3-numpy is unsafe, trusting Python memory is valid.
fn as_array2_f64<'py>(obj: &'py PyAny) -> PyResult<ArrayView2<'py, f64>> {
    let pyarray = obj.downcast::<PyArray2<f64>>()?;
    let view = unsafe { pyarray.as_array() };
    Ok(view)
}

/// Similarly, for 1D arrays.
fn as_array1_f64<'py>(obj: &'py PyAny) -> PyResult<ArrayView1<'py, f64>> {
    let pyarray = obj.downcast::<PyArray1<f64>>()?;
    let view = unsafe { pyarray.as_array() };
    Ok(view)
}

/// Extracts (beta, cov_beta, exog_names, X) from the Python Probit model via direct bridging.
/// For zero-copy, params, cov_params(), and model.exog must be NumPy arrays, not Pandas.
fn extract_probit_model_components<'py>(
    _py: Python<'py>,
    probit_model: &'py PyAny,
) -> PyResult<(Array1<f64>, Array2<f64>, Vec<String>, Array2<f64>)> {
    // Beta (params)
    let params_obj = probit_model.getattr("params")?;
    let beta_view = as_array1_f64(params_obj)?;
    let beta = beta_view.to_owned(); // Owned Array1

    // Cov beta
    let cov_obj = probit_model.call_method0("cov_params")?;
    let cov_view = as_array2_f64(cov_obj)?;
    let cov_beta = cov_view.to_owned(); // Owned Array2

    // exog_names
    let exog_names_py: Vec<String> = probit_model
        .getattr("model")?
        .getattr("exog_names")?
        .extract()?;

    // X
    let x_obj = probit_model.getattr("model")?.getattr("exog")?;
    let x_view = as_array2_f64(x_obj)?;
    let X = x_view.to_owned(); // Owned Array2

    Ok((beta, cov_beta, exog_names_py, X))
}


/// Calculates Average Marginal Effects (AME) for a Probit model
#[pyfunction]
fn ame<'py>(
    py: Python<'py>,
    probit_model: &'py PyAny,  // Our Python Probit model
    chunk_size: Option<usize>, // Lets users process data in chunks (optional!)
) -> PyResult<&'py PyAny> {

    // ====================== STEP 1: Get Model Ingredients ======================
    // Think of this like gathering all the ingredients before cooking
    
    // Get model parameters (β coefficients)
    let params_pyarray: &PyArray1<f64> = probit_model.getattr("params")?.downcast()?;
    let beta = unsafe { params_pyarray.as_array() };  // Borrow numpy array directly
    
    // Get covariance matrix of parameters
    let cov_pyarray: &PyArray2<f64> = probit_model.call_method0("cov_params")?.downcast()?;
    let cov_beta = unsafe { cov_pyarray.as_array() };  // Another zero-copy view
    
    // Get feature names (like column names from DataFrame)
    let exog_names: Vec<String> = probit_model
        .getattr("model")?
        .getattr("exog_names")?
        .extract()?;
    
    // Get actual feature data (X matrix)
    let x_pyarray: &PyArray2<f64> = probit_model.getattr("model")?.getattr("exog")?.downcast()?;
    let X = unsafe { x_pyarray.as_array() };  // Our main data matrix view

    let (n, k) = (X.nrows(), X.ncols());  // n=number of samples, k=number of features
    let chunk = chunk_size.unwrap_or(n);  // Use whole dataset if chunk_size not specified

    // ====================== STEP 2: Identify Special Columns ======================
    // Some columns need special treatment (like intercepts and yes/no features)

    // Find intercept columns (like "const" or "intercept")
    let intercept_indices: Vec<usize> = exog_names
        .iter()
        .enumerate()
        .filter_map(|(i, nm)| {
            let ln = nm.to_lowercase();
            if ln == "const" || ln == "intercept" { Some(i) } else { None }
        })
        .collect();

    // Find dummy variables (columns with only 0s and 1s)
    let is_discrete: Vec<usize> = exog_names
        .iter()
        .enumerate()
        .filter_map(|(j, _)| {
            // Skip intercepts since they're handled separately
            intercept_indices.contains(&j).then(|| None).unwrap_or_else(|| {
                // Check if all values are 0 or 1 (like a yes/no feature)
                X.column(j).iter().all(|&v| v == 0.0 || v == 1.0).then_some(j)
            })
        })
        .collect();

    // ====================== STEP 3: Setup Calculation Tools ======================
    // Like getting your measuring cups and mixing bowls ready
    
    // These will accumulate results as we process chunks
    let mut sum_ame = vec![0.0; k];          // Stores AME sums for each feature
    let mut partial_jl_sums = vec![0.0; k * k]; // For covariance calculations
    let normal = Normal::new(0.0, 1.0).unwrap(); // Our probability calculator

    // ====================== STEP 4: Process Data in Chunks ======================
    // Like eating a pizza slice by slice instead of all at once
    let mut idx_start = 0;
    while idx_start < n {
        let idx_end = (idx_start + chunk).min(n); // Where this chunk ends
        
        // Take a slice of our data (zero-copy!)
        let x_chunk = X.slice(ndarray::s![idx_start..idx_end, ..]);
        
        // Calculate linear predictor (z = Xβ) for this chunk
        let z_chunk = x_chunk.dot(&beta);
        // Get PDF values (φ(z)) for all observations
        let phi_vals = z_chunk.mapv(|z| normal.pdf(z));

        // ------ Handling Discrete Features (like yes/no columns) ------
        for &j in &is_discrete {
            // Smart calculation using vector math instead of making copies:
            let xj_col = x_chunk.column(j);  // Current values of this feature
            let beta_j = beta[j];            // Coefficient for this feature
            
            // Calculate what z would be if this feature was always 1 vs always 0
            let delta_j1 = (1.0 - &xj_col).mapv(|x| x * beta_j); // Difference if set to 1
            let delta_j0 = xj_col.mapv(|x| -x * beta_j);         // Difference if set to 0
            let z_j1 = &z_chunk + &delta_j1; // Hypothetical z if feature=1
            let z_j0 = &z_chunk + &delta_j0; // Hypothetical z if feature=0

            // Calculate AME contribution from this feature
            let cdf_diff_sum = z_j1.mapv(|z| normal.cdf(z)).sum() 
                               - z_j0.mapv(|z| normal.cdf(z)).sum();
            sum_ame[j] += cdf_diff_sum;

            // Calculate how changes affect uncertainty (for standard errors)
            let pdf_j1 = z_j1.mapv(|z| normal.pdf(z)); // PDF if feature=1
            let pdf_j0 = z_j0.mapv(|z| normal.pdf(z)); // PDF if feature=0
            
            // Update gradient calculations for covariance
            for l in 0..k {
                let grad = if l == j {
                    // Special case when feature affects itself
                    pdf_j1.sum()
                } else {
                    // General case for other features
                    let xl_col = x_chunk.column(l); // Values of other feature
                    (&pdf_j1 - &pdf_j0).dot(&xl_col)
                };
                partial_jl_sums[j * k + l] += grad;
            }
        }

        // ------ Handling Continuous Features (like age or income) ------
        for j in 0..k {
            // Skip intercepts and discrete features we already handled
            if intercept_indices.contains(&j) || is_discrete.contains(&j) {
                continue;
            }

            let beta_j = beta[j]; // Coefficient for this feature
            
            // Main AME calculation for continuous features
            sum_ame[j] += beta_j * phi_vals.sum();

            // Calculate gradient contributions for uncertainty
            for l in 0..k {
                let grad = if j == l {
                    // Direct effect of this feature on itself
                    phi_vals.sum()
                } else {
                    // Interactive effect with other features
                    -beta_j * (&z_chunk * &x_chunk.column(l)).dot(&phi_vals)
                };
                partial_jl_sums[j * k + l] += grad;
            }
        }

        idx_start = idx_end; // Move to next chunk
    }

    // ====================== STEP 5: Final Calculations ======================
    // Baking the final results from our prepared ingredients
    
    // Average out the accumulated sums
    let ame: Vec<f64> = sum_ame.iter().map(|v| v / n as f64).collect();
    
    // Prepare gradient matrix for covariance calculation
    let mut grad_ame = Array2::zeros((k, k));
    for j in 0..k {
        for l in 0..k {
            grad_ame[(j, l)] = partial_jl_sums[j * k + l] / n as f64;
        }
    }
    
    // Calculate covariance matrix of AMEs
    let cov_ame = grad_ame.dot(&cov_beta).dot(&grad_ame.t());
    
    // Get standard errors from covariance diagonal
    let var_ame: Vec<f64> = cov_ame.diag().iter().map(|&v| v.max(0.0)).collect();
    let se_ame: Vec<f64> = var_ame.iter().map(|v| v.sqrt()).collect();

    // ====================== STEP 6: Prepare Results ======================
    // Plating our dish for serving to Python
    
    let (mut dy_dx, mut se_err, mut z_vals, mut p_vals, mut sig) = 
        (Vec::new(), Vec::new(), Vec::new(), Vec::new(), Vec::new());
    let mut names = Vec::new();
    
    for j in 0..k {
        if intercept_indices.contains(&j) { 
            continue; // Skip intercepts in final output
        }
        
        dy_dx.push(ame[j]);
        se_err.push(se_ame[j]);
        
        // Calculate z-score (but handle zero division)
        let z = if se_ame[j] > 0.0 { 
            ame[j] / se_ame[j] 
        } else { 
            f64::NAN  // Mark invalid calculations
        };
        z_vals.push(z);
        
        // Calculate p-value using normal distribution
        let p = 2.0 * (1.0 - normal.cdf(z.abs()));
        p_vals.push(p);
        sig.push(add_significance_stars(p));
        
        names.push(exog_names[j].clone()); // Keep feature names
    }

    // ====================== STEP 7: Create Pandas DataFrame ======================
    // Packaging our results in a nice Python-friendly format
    
    let pd = py.import("pandas")?; // Get pandas module
    let data = PyDict::new(py);    // Create dictionary for DataFrame data
    
    // Add each column to our DataFrame dictionary
    data.set_item("dy/dx", dy_dx)?;          // Marginal effects
    data.set_item("Std. Err", se_err)?;      // Standard errors
    data.set_item("z", z_vals)?;             // Z-scores
    data.set_item("Pr(>|z|)", p_vals)?;      // p-values
    data.set_item("Significance", sig)?;     // Stars
    
    // Create keyword arguments for DataFrame constructor
    let kwargs = PyDict::new(py);
    kwargs.set_item("data", data)?;       // Our calculated data
    kwargs.set_item("index", names)?;     // Feature names as index

    // Finally create the DataFrame and return it
    pd.call_method("DataFrame", (), Some(kwargs))
}


// ------------------ Matrix Inversion with Partial Pivoting ------------------

fn invert_matrix_partial_pivot(mat: &Array2<f64>) -> Option<Array2<f64>> {
    let n = mat.nrows();
    if mat.ncols() != n {
        return None;
    }
    let mut aug = Array2::<f64>::zeros((n, 2*n));
    for r in 0..n {
        for c in 0..n {
            aug[[r, c]] = mat[[r, c]];
        }
        aug[[r, r + n]] = 1.0;
    }
    // Forward elimination
    for i in 0..n {
        let mut pivot_row = i;
        let mut pivot_val = aug[[i, i]].abs();
        for r in (i+1)..n {
            let check_val = aug[[r, i]].abs();
            if check_val > pivot_val {
                pivot_val = check_val;
                pivot_row = r;
            }
        }
        if pivot_val < 1e-14 {
            return None;
        }
        if pivot_row != i {
            for c in 0..2*n {
                let tmp = aug[[i, c]];
                aug[[i, c]] = aug[[pivot_row, c]];
                aug[[pivot_row, c]] = tmp;
            }
        }
        let pivot = aug[[i, i]];
        for c in i..2*n {
            aug[[i, c]] /= pivot;
        }
        for r in (i+1)..n {
            let factor = aug[[r, i]];
            for c in i..2*n {
                aug[[r, c]] -= factor * aug[[i, c]];
            }
        }
    }
    // Back-substitution
    for i in (0..n).rev() {
        for r in 0..i {
            let factor = aug[[r, i]];
            for c in i..2*n {
                aug[[r, c]] -= factor * aug[[i, c]];
            }
        }
    }
    // Extract right half
    let mut inv = Array2::<f64>::zeros((n, n));
    for r in 0..n {
        for c in 0..n {
            inv[[r, c]] = aug[[r, c + n]];
        }
    }
    Some(inv)
}

fn mat_vec_mul(mat: &Array2<f64>, vec: &Array1<f64>) -> Array1<f64> {
    let k = vec.len();
    let mut out = Array1::<f64>::zeros(k);
    for i in 0..k {
        for j in 0..k {
            out[i] += mat[[i, j]] * vec[j];
        }
    }
    out
}

// ------------------ Minimal Probit Model -------------------------------------

struct Probit {
    endog: Array1<f64>,
    exog: Array2<f64>,
    normal: Normal,
}

impl Probit {
    fn new(endog: Array1<f64>, exog: Array2<f64>) -> Self {
        Probit {
            endog,
            exog,
            normal: Normal::new(0.0, 1.0).unwrap(),
        }
    }
    fn cdf(&self, x: f64) -> f64 {
        let c = self.normal.cdf(x);
        c.max(1e-15).min(1.0 - 1e-15)
    }
    fn pdf(&self, x: f64) -> f64 {
        self.normal.pdf(x)
    }
    fn xbeta(&self, params: &Array1<f64>, i: usize) -> f64 {
        let row = self.exog.row(i);
        let mut sum = 0.0;
        for j in 0..row.len() {
            sum += row[j] * params[j];
        }
        sum
    }
    fn loglike(&self, params: &Array1<f64>) -> f64 {
        let nobs = self.endog.len();
        let mut ll = 0.0;
        for i in 0..nobs {
            let q = 2.0 * self.endog[i] - 1.0;
            let z = q * self.xbeta(params, i);
            ll += self.cdf(z).ln();
        }
        ll
    }
    fn score(&self, params: &Array1<f64>) -> Array1<f64> {
        let kvars = self.exog.ncols();
        let nobs = self.endog.len();
        let mut grad = Array1::<f64>::zeros(kvars);
        for i in 0..nobs {
            let q = 2.0 * self.endog[i] - 1.0;
            let z = q * self.xbeta(params, i);
            let ratio = (q * self.pdf(z)) / self.cdf(z);
            let row = self.exog.row(i);
            for j in 0..kvars {
                grad[j] += ratio * row[j];
            }
        }
        grad
    }
    fn hessian(&self, params: &Array1<f64>) -> Array2<f64> {
        let (nobs, kvars) = (self.endog.len(), self.exog.ncols());
        let mut hess = Array2::<f64>::zeros((kvars, kvars));
        for i in 0..nobs {
            let q = 2.0 * self.endog[i] - 1.0;
            let xbeta = self.xbeta(params, i);
            let z = q * xbeta;
            let cdf_ = self.cdf(z);
            let pdf_ = self.pdf(z);
            let lambda = (q * pdf_) / cdf_;
            let val = lambda * (lambda + xbeta);
            let row = self.exog.row(i);
            for r in 0..kvars {
                for c in 0..kvars {
                    hess[[r, c]] -= val * row[r] * row[c];
                }
            }
        }
        hess
    }
    fn fit_naive_newton(&self, max_iter: usize, tol: f64) -> (Array1<f64>, f64, bool, usize) {
        let k = self.exog.ncols();
        let mut params = Array1::<f64>::zeros(k);
        let mut ll_old = self.loglike(&params);
        let mut converged = false;
        let mut iter_used = 0;
        for iter in 0..max_iter {
            iter_used = iter;
            let grad = self.score(&params);
            let hess = self.hessian(&params);
            match invert_matrix_partial_pivot(&hess) {
                Some(inv_hess) => {
                    let step = mat_vec_mul(&inv_hess, &grad);
                    let new_params = &params - &step;
                    let ll_new = self.loglike(&new_params);
                    if (ll_new - ll_old).abs() < tol {
                        params = new_params;
                        ll_old = ll_new;
                        converged = true;
                        break;
                    }
                    params = new_params;
                    ll_old = ll_new;
                }
                None => {
                    eprintln!("Hessian near singular at iteration {iter}");
                    break;
                }
            }
        }
        (params, ll_old, converged, iter_used)
    }
}

// ------------------ RustProbitResults PyClass  ------------------------------

#[pyclass]
struct RustProbitResults {
    #[pyo3(get)]
    params: Py<PyArray1<f64>>,   // final coefficients
    cov: Py<PyArray2<f64>>,      // covariance matrix
    exog_py: Py<PyArray2<f64>>,
    endog_py: Py<PyArray1<f64>>,
    exog_names: Vec<String>,

    pub loglike: f64,
    pub iterations: usize,
    pub converged: bool,
}

#[pymethods]
impl RustProbitResults {
    /// Return an owned handle to the covariance array (no lifetime issues).
    fn cov_params(&self) -> Py<PyArray2<f64>> {
        self.cov.clone()
    }

    /// Return a Python dict with .exog, .endog, .exog_names
    fn model(&self, py: Python<'_>) -> Py<PyDict> {
        let d = PyDict::new(py);
        d.set_item("exog", self.exog_py.clone_ref(py)).unwrap();
        d.set_item("endog", self.endog_py.clone_ref(py)).unwrap();
        d.set_item("exog_names", &self.exog_names).unwrap();
        d.into()
    }
}

// ------------------ White & Cluster Helpers (unchanged) ---------------------

fn calc_white_crossprod(s_obs: &Array2<f64>) -> Array2<f64> {
    let (nobs, k) = (s_obs.nrows(), s_obs.ncols());
    let mut M = Array2::<f64>::zeros((k, k));
    for i in 0..nobs {
        for r in 0..k {
            for c in 0..k {
                M[[r, c]] += s_obs[[i, r]] * s_obs[[i, c]];
            }
        }
    }
    M
}

fn combine_cluster_keys(cluster_cols: &Array2<f64>) -> Vec<String> {
    let (nobs, ncols) = (cluster_cols.nrows(), cluster_cols.ncols());
    let mut keys = Vec::with_capacity(nobs);
    for i in 0..nobs {
        let mut s = String::new();
        for j in 0..ncols {
            if j > 0 {
                s.push('|');
            }
            write!(&mut s, "{:.4}", cluster_cols[[i, j]]).unwrap();
        }
        keys.push(s);
    }
    keys
}

// ------------------ The Fit Function  ---------------------------------------

#[pyfunction]
#[allow(clippy::too_many_arguments)]
fn fit_probit(
    py: Python<'_>,
    endog_py: &PyArray1<f64>,
    exog_py: &PyArray2<f64>,
    max_iter: Option<usize>,
    tol: Option<f64>,
    robust: Option<bool>,
    cluster_vars: Option<&PyAny>,
) -> PyResult<RustProbitResults> {
    // Must call `unsafe { as_array() }` to avoid the E0133 error:
    let endog = unsafe { endog_py.as_array() }.to_owned();
    let exog = unsafe { exog_py.as_array() }.to_owned();

    let max_iter = max_iter.unwrap_or(50);
    let tol = tol.unwrap_or(1e-8);
    let do_robust = robust.unwrap_or(false);

    // Fit model
    let model = Probit::new(endog.clone(), exog.clone());
    let (params, llf, converged, iterations) = model.fit_naive_newton(max_iter, tol);

    // Hessian => classical Cov = -H^-1
    let hess_final = model.hessian(&params);
    let maybe_inv_hess = invert_matrix_partial_pivot(&hess_final);
    let kvars = exog.ncols();
    let mut hess_inv = match maybe_inv_hess {
        Some(m) => m,
        None => {
            eprintln!("Unable to invert Hessian => returning identity for Cov");
            Array2::<f64>::eye(kvars)
        }
    };
    for x in hess_inv.iter_mut() {
        *x = -*x;  // classical
    }
    let mut cov_final = hess_inv.clone();

    // If robust or cluster => White or cluster-robust
    if do_robust {
        // build s_obs
        let nobs = endog.len();
        let mut s_obs_mat = Array2::<f64>::zeros((nobs, kvars));
        for i in 0..nobs {
            let q = 2.0 * endog[i] - 1.0;
            let z = q * model.xbeta(&params, i);
            let ratio = (q * model.pdf(z)) / model.cdf(z);
            for j in 0..kvars {
                s_obs_mat[[i, j]] = ratio * exog[[i, j]];
            }
        }

        let final_mat = if let Some(obj) = cluster_vars {
            if obj.is_none() {
                calc_white_crossprod(&s_obs_mat)
            } else {
                let arr_f64 = obj.downcast::<PyArray2<f64>>()?;
                let cluster_view = unsafe { arr_f64.as_array() }.to_owned();
                if cluster_view.nrows() != nobs {
                    return Err(pyo3::exceptions::PyValueError::new_err(
                        format!("cluster array rows={}, mismatch nobs={}", cluster_view.nrows(), nobs)
                    ));
                }
                let keys = combine_cluster_keys(&cluster_view);
                let mut group_sums: HashMap<String, Array1<f64>> = HashMap::new();
                for (i, key) in keys.iter().enumerate() {
                    let e = group_sums.entry(key.clone()).or_insert_with(|| Array1::<f64>::zeros(kvars));
                    for j in 0..kvars {
                        e[j] += s_obs_mat[[i, j]];
                    }
                }
                let mut M = Array2::<f64>::zeros((kvars, kvars));
                for (_, sumv) in group_sums {
                    for r in 0..kvars {
                        for c in 0..kvars {
                            M[[r, c]] += sumv[r] * sumv[c];
                        }
                    }
                }
                M
            }
        } else {
            // White
            calc_white_crossprod(&s_obs_mat)
        };

        // Cov_robust = ( +H^-1 ) * final_mat * ( +H^-1 )
        // But we have cov_final = -H^-1 => so +H^-1 = -cov_final
        let mut h_inv_pos = cov_final.clone();
        for x in h_inv_pos.iter_mut() {
            *x = -*x;
        }
        let a = h_inv_pos.dot(&final_mat);
        let cov_robust = a.dot(&h_inv_pos);
        cov_final = cov_robust;
    }

    // Convert to Py objects
    let params_py = params.clone().into_pyarray(py).to_owned();
    let cov_py = cov_final.into_pyarray(py).to_owned();
    let exog_py_ = exog.into_pyarray(py).to_owned();
    let endog_py_ = endog.into_pyarray(py).to_owned();

    let mut exog_names = Vec::new();
    for j in 0..kvars {
        exog_names.push(format!("x{}", j));
    }

    let results = RustProbitResults {
        params: params_py,
        cov: cov_py,
        exog_py: exog_py_,
        endog_py: endog_py_,
        exog_names,
        loglike: llf,
        iterations,
        converged,
    };

    Ok(results)
}


/// A Python module implemented in Rust.
#[pymodule]
fn rustats(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(ame, m)?)?;
    // New Probit "fit_probit" function
    m.add_function(wrap_pyfunction!(fit_probit, m)?)?;
    Ok(())
}
