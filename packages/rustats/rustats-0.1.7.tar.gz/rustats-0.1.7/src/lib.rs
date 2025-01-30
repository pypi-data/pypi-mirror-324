use pyo3::prelude::*;
use pyo3::types::{PyAny, PyDict};
use pyo3::wrap_pyfunction;

use numpy::{PyArray1, PyArray2, IntoPyArray};
use ndarray::{Array1, Array2, ArrayView1, ArrayView2};
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


// -----------------------------------------------------------------------------
// Minimal BFGS approach without repeated Hessian
// -----------------------------------------------------------------------------
fn bfgs<F, G>(
    x0: Array1<f64>,
    max_iter: usize,
    tol: f64,
    grad_fn: G,
    ll_fn: F,
) -> (Array1<f64>, f64, bool, usize)
where
    F: Fn(&Array1<f64>) -> f64,
    G: Fn(&Array1<f64>) -> Array1<f64>,
{
    let k = x0.len();
    let mut x = x0;
    let mut ll_old = ll_fn(&x);
    let mut g_old = grad_fn(&x);

    let mut B = Array2::<f64>::eye(k);

    let mut converged = false;
    let mut iter_used = 0;

    for iter in 0..max_iter {
        iter_used = iter;

        // direction = -B*g
        let p = -B.dot(&g_old);

        // step-halving line search
        let mut step_size = 1.0;
        let old_ll = ll_old;

        let mut x_new = &x + &p.mapv(|v| v * step_size);
        let mut ll_new = ll_fn(&x_new);

        let mut halving_count = 0;
        while ll_new < old_ll && halving_count < 10 {
            step_size *= 0.5;
            x_new = &x + &p.mapv(|v| v * step_size);
            ll_new = ll_fn(&x_new);
            halving_count += 1;
        }

        let g_new = grad_fn(&x_new);
        let diff_ll = (ll_new - ll_old).abs();

        // BFGS update
        let s = &x_new - &x;
        let y = &g_new - &g_old;
        let ys = y.dot(&s);

        if ys.abs() > 1e-14 {
            // shape(k,1) for s, y
            let s_mat = s.clone().into_shape((s.len(), 1)).unwrap();
            let y_mat = y.clone().into_shape((y.len(), 1)).unwrap();

            // term1 = (s s^T) / (s^T y)
            let s_sT = s_mat.dot(&s_mat.t());
            let term1 = s_sT.mapv(|v| v / ys);

            // term2 = (B y)(B y)^T / (y^T B y)
            let By = B.dot(&y);
            let By_len = By.len();
            let By_mat = By.clone().into_shape((By_len, 1)).unwrap();

            let yT_B = y.clone().into_shape((1, y.len())).unwrap().dot(&B);
            let denom2 = yT_B.dot(&By_mat)[[0, 0]];
            if denom2.abs() > 1e-14 {
                let By_ByT = By_mat.dot(&By_mat.t());
                let term2 = By_ByT.mapv(|v| v / denom2);

                // B = B + term1 - term2
                for r in 0..k {
                    for c in 0..k {
                        B[[r, c]] += term1[[r, c]] - term2[[r, c]];
                    }
                }
            }
        }

        x = x_new;
        g_old = g_new;
        ll_old = ll_new;

        if diff_ll < tol {
            converged = true;
            break;
        }
    }

    (x, ll_old, converged, iter_used)
}

// -----------------------------------------------------------------------------
// Minimal Probit
// -----------------------------------------------------------------------------
struct Probit {
    endog: Array1<f64>,
    exog: Array2<f64>,
    dist: Normal,
}

impl Probit {
    fn new(endog: Array1<f64>, exog: Array2<f64>) -> Self {
        Probit {
            endog,
            exog,
            dist: Normal::new(0.0, 1.0).unwrap(),
        }
    }

    fn cdf(&self, z: f64) -> f64 {
        let c = self.dist.cdf(z);
        c.max(1e-15).min(1.0 - 1e-15)
    }

    fn pdf(&self, z: f64) -> f64 {
        self.dist.pdf(z)
    }

    fn xbeta(&self, params: &Array1<f64>, i: usize) -> f64 {
        let row = self.exog.row(i);
        let mut val = 0.0;
        for j in 0..row.len() {
            val += row[j] * params[j];
        }
        val
    }

    fn loglike(&self, params: &Array1<f64>) -> f64 {
        let mut ll = 0.0;
        let nobs = self.endog.len();
        for i in 0..nobs {
            let q = 2.0*self.endog[i] - 1.0;
            let z = q * self.xbeta(params, i);
            ll += self.cdf(z).ln();
        }
        ll
    }

    fn grad(&self, params: &Array1<f64>) -> Array1<f64> {
        let nobs = self.endog.len();
        let kvars = self.exog.ncols();
        let mut g = Array1::<f64>::zeros(kvars);
        for i in 0..nobs {
            let q = 2.0*self.endog[i] - 1.0;
            let xbeta = self.xbeta(params, i);
            let ratio = (q * self.pdf(q*xbeta)) / self.cdf(q*xbeta);
            let row = self.exog.row(i);
            for j in 0..kvars {
                g[j] += ratio * row[j];
            }
        }
        g
    }

    // For final Cov => -H^-1
    fn hessian(&self, params: &Array1<f64>) -> Array2<f64> {
        let nobs = self.endog.len();
        let kvars = self.exog.ncols();
        let mut hess = Array2::<f64>::zeros((kvars,kvars));
        for i in 0..nobs {
            let q = 2.0*self.endog[i] - 1.0;
            let xbeta = self.xbeta(params, i);
            let lam = (q * self.pdf(q*xbeta)) / self.cdf(q*xbeta);
            let val = lam * (lam + xbeta);
            let row = self.exog.row(i);
            for r in 0..kvars {
                for c in 0..kvars {
                    hess[[r,c]] -= val * row[r]*row[c];
                }
            }
        }
        hess
    }

    fn fit_bfgs(&self, max_iter: usize, tol: f64) -> (Array1<f64>, f64, bool, usize) {
        let k = self.exog.ncols();
        let x0 = Array1::<f64>::zeros(k);
        let ll_fn = |p: &Array1<f64>| self.loglike(p);
        let grad_fn = |p: &Array1<f64>| self.grad(p);
        bfgs(x0, max_iter, tol, grad_fn, ll_fn)
    }
}

// -----------------------------------------------------------------------------
// partial pivot invert => for final Cov
// -----------------------------------------------------------------------------
fn invert_matrix_partial_pivot(mat: &Array2<f64>) -> Option<Array2<f64>> {
    let n = mat.nrows();
    if mat.ncols() != n {
        return None;
    }
    let mut aug = Array2::<f64>::zeros((n, 2*n));
    for r in 0..n {
        for c in 0..n {
            aug[[r,c]] = mat[[r,c]];
        }
        aug[[r,r+n]] = 1.0;
    }
    // forward elimination
    for i in 0..n {
        let mut pivot_row = i;
        let mut pivot_val = aug[[i,i]].abs();
        for r in (i+1)..n {
            let check_val = aug[[r,i]].abs();
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
                let tmp = aug[[i,c]];
                aug[[i,c]] = aug[[pivot_row,c]];
                aug[[pivot_row,c]] = tmp;
            }
        }
        let pivot = aug[[i,i]];
        for c in i..2*n {
            aug[[i,c]] /= pivot;
        }
        for r in (i+1)..n {
            let factor = aug[[r,i]];
            for c in i..2*n {
                aug[[r,c]] -= factor * aug[[i,c]];
            }
        }
    }
    // back-substitution
    for i in (0..n).rev() {
        for r in 0..i {
            let factor = aug[[r,i]];
            for c in i..2*n {
                aug[[r,c]] -= factor * aug[[i,c]];
            }
        }
    }
    let mut inv = Array2::<f64>::zeros((n,n));
    for r in 0..n {
        for c in 0..n {
            inv[[r,c]] = aug[[r,c+n]];
        }
    }
    Some(inv)
}

// -----------------------------------------------------------------------------
// White & cluster
// -----------------------------------------------------------------------------
fn calc_white_crossprod(s_obs: &Array2<f64>) -> Array2<f64> {
    let (nobs, k) = (s_obs.nrows(), s_obs.ncols());
    let mut M = Array2::<f64>::zeros((k,k));
    for i in 0..nobs {
        for r in 0..k {
            for c in 0..k {
                M[[r,c]] += s_obs[[i,r]]*s_obs[[i,c]];
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
            if j>0 { s.push('|'); }
            write!(&mut s, "{:.4}", cluster_cols[[i,j]]).unwrap();
        }
        keys.push(s);
    }
    keys
}

// -----------------------------------------------------------------------------
// PyO3 model / results
// -----------------------------------------------------------------------------
#[pyclass]
#[derive(Clone)]
struct RustProbitModel {
    exog_: Py<PyArray2<f64>>,
    endog_: Py<PyArray1<f64>>,
    exog_names_: Vec<String>,
}

#[pymethods]
impl RustProbitModel {
    #[getter]
    fn exog(&self) -> Py<PyArray2<f64>> {
        self.exog_.clone()
    }
    #[getter]
    fn endog(&self) -> Py<PyArray1<f64>> {
        self.endog_.clone()
    }
    #[getter]
    fn exog_names(&self) -> Vec<String> {
        self.exog_names_.clone()
    }
}

#[pyclass]
struct RustProbitResults {
    params_: Py<PyArray1<f64>>,
    cov_: Py<PyArray2<f64>>,
    model_: RustProbitModel,
    loglike_: f64,
    iterations: usize,
    converged: bool,
}

#[pymethods]
impl RustProbitResults {
    #[getter]
    fn params(&self) -> Py<PyArray1<f64>> {
        self.params_.clone()
    }

    fn cov_params(&self) -> Py<PyArray2<f64>> {
        self.cov_.clone()
    }

    #[getter]
    fn model(&self) -> RustProbitModel {
        self.model_.clone()
    }

    #[getter]
    fn loglike(&self) -> f64 {
        self.loglike_
    }

    #[getter]
    fn iterations(&self) -> usize {
        self.iterations
    }

    #[getter]
    fn converged(&self) -> bool {
        self.converged
    }
}

// -----------------------------------------------------------------------------
// fit_probit function => BFGS, final Cov, robust/cluster
// -----------------------------------------------------------------------------
#[pyfunction]
fn fit_probit(
    py: Python<'_>,
    endog_py: &PyAny,
    exog_py: &PyArray2<f64>,
    max_iter: Option<usize>,
    tol: Option<f64>,
    robust: Option<bool>,
    cluster_vars: Option<&PyAny>,
) -> PyResult<RustProbitResults> {
    // Flatten
    let endog: Array1<f64> = {
        let arr_shape = endog_py.getattr("shape")?.extract::<(usize, Option<usize>)>()?;
        match arr_shape {
            (nobs, None) => {
                let arr_1d = endog_py.downcast::<PyArray1<f64>>()?;
                unsafe { arr_1d.as_array().to_owned() }
            }
            (nobs, Some(1)) => {
                let arr_2d = endog_py.downcast::<PyArray2<f64>>()?;
                let arr_view = unsafe { arr_2d.as_array() };
                arr_view.column(0).to_owned()
            }
            (r, c) => {
                return Err(pyo3::exceptions::PyValueError::new_err(
                    format!("endog must be shape (nobs,) or (nobs,1). got=({},{:?})", r,c)
                ));
            }
        }
    };

    let exog = unsafe { exog_py.as_array() }.to_owned();
    let max_iter = max_iter.unwrap_or(35);
    let tol = tol.unwrap_or(1e-6);
    let do_robust = robust.unwrap_or(false);

    // BFGS
    let model_data = Probit::new(endog.clone(), exog.clone());
    let (params, llf, converged, iterations) = model_data.fit_bfgs(max_iter, tol);

    // final classical Cov => -H^-1
    let hess_final = model_data.hessian(&params);
    let maybe_inv = invert_matrix_partial_pivot(&hess_final);
    let kvars = exog.ncols();
    let mut hess_inv = match maybe_inv {
        Some(m) => m,
        None => {
            eprintln!("Hessian singular => identity for Cov");
            Array2::<f64>::eye(kvars)
        }
    };
    for x in hess_inv.iter_mut() {
        *x = -*x;
    }
    let mut cov_final = hess_inv.clone();

    // robust/cluster
    if do_robust {
        let nobs = endog.len();
        let mut s_obs_mat = Array2::<f64>::zeros((nobs,kvars));
        for i in 0..nobs {
            let q = 2.0*endog[i] - 1.0;
            let z = q * model_data.xbeta(&params, i);
            let ratio = (q * model_data.pdf(z)) / model_data.cdf(z);
            for j in 0..kvars {
                s_obs_mat[[i,j]] = ratio * exog[[i,j]];
            }
        }
        let final_mat = if let Some(obj) = cluster_vars {
            if obj.is_none() {
                calc_white_crossprod(&s_obs_mat)
            } else {
                // cluster
                let arr_2d = obj.downcast::<PyArray2<f64>>()?;
                let cluster_view = unsafe { arr_2d.as_array() }.to_owned();
                if cluster_view.nrows() != nobs {
                    return Err(pyo3::exceptions::PyValueError::new_err(
                        format!("cluster mismatch: got {} rows, nobs={}", cluster_view.nrows(), nobs)
                    ));
                }
                let keys = combine_cluster_keys(&cluster_view);
                let mut group_sums: HashMap<String, Array1<f64>> = HashMap::new();
                for (i, key) in keys.iter().enumerate() {
                    let e = group_sums.entry(key.clone()).or_insert_with(|| Array1::<f64>::zeros(kvars));
                    for j in 0..kvars {
                        e[j] += s_obs_mat[[i,j]];
                    }
                }
                let mut M = Array2::<f64>::zeros((kvars,kvars));
                for (_, sumv) in group_sums {
                    for r in 0..kvars {
                        for c in 0..kvars {
                            M[[r,c]] += sumv[r]*sumv[c];
                        }
                    }
                }
                M
            }
        } else {
            calc_white_crossprod(&s_obs_mat)
        };

        // Cov_robust = +H^-1 * final_mat * +H^-1
        let mut h_inv_pos = cov_final.clone();
        for x in h_inv_pos.iter_mut() {
            *x = -*x; // +H^-1
        }
        let a = h_inv_pos.dot(&final_mat);
        cov_final = a.dot(&h_inv_pos);
    }

    let params_py = params.clone().into_pyarray(py).to_owned();
    let cov_py = cov_final.into_pyarray(py).to_owned();
    let exog_py_ = exog.clone().into_pyarray(py).to_owned();
    let endog_py_ = endog.clone().into_pyarray(py).to_owned();

    let mut exog_names = Vec::new();
    for j in 0..kvars {
        exog_names.push(format!("x{}", j));
    }

    let rust_model = RustProbitModel {
        exog_: exog_py_,
        endog_: endog_py_,
        exog_names_: exog_names,
    };

    let result = RustProbitResults {
        params_: params_py,
        cov_: cov_py,
        model_: rust_model,
        loglike_: llf,
        iterations,
        converged,
    };

    Ok(result)
}

/// A Python module implemented in Rust.
#[pymodule]
fn rustats(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(ame, m)?)?;
    // New Probit "fit_probit" function
    m.add_function(wrap_pyfunction!(fit_probit, m)?)?;
    Ok(())
}
