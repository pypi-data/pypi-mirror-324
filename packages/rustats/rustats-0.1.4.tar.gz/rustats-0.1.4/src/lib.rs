use pyo3::prelude::*;
use pyo3::types::{IntoPyDict, PyAny, PyDict, PyList};
use pyo3::wrap_pyfunction;

use numpy::{PyArray1, PyArray2};
use ndarray::{Array1, Array2, ArrayView1, ArrayView2, s};
use statrs::distribution::{Continuous, Normal, ContinuousCDF};

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

/// A direct "naive" Probit model with no pivoting or offset, purely demonstration.
struct Probit {
    endog: Array1<f64>,
    exog: Array2<f64>,
    standard_normal: Normal,
}

impl Probit {
    fn new(endog: Array1<f64>, exog: Array2<f64>) -> Self {
        Self {
            endog,
            exog,
            standard_normal: Normal::new(0.0, 1.0).unwrap(),
        }
    }

    fn cdf(&self, x: f64) -> f64 {
        self.standard_normal.cdf(x).max(1e-15).min(1.0 - 1e-15)
    }

    fn pdf(&self, x: f64) -> f64 {
        self.standard_normal.pdf(x)
    }

    /// Predict linear => Xβ
    fn predict_linear(&self, params: &Array1<f64>, i: usize) -> f64 {
        let mut val = 0.0;
        let row = self.exog.row(i);
        for j in 0..row.len() {
            val += row[j] * params[j];
        }
        val
    }

    /// Log-likelihood: sum( ln Phi( q_i X_i' β ) ), q_i=2y_i-1
    fn loglike(&self, params: &Array1<f64>) -> f64 {
        let mut ll = 0.0;
        for i in 0..self.endog.len() {
            let q_i = 2.0 * self.endog[i] - 1.0;
            let z = q_i * self.predict_linear(params, i);
            ll += self.cdf(z).ln();
        }
        ll
    }

    /// Gradient => X' * [ (q_i φ(q_iXβ)) / Φ(q_iXβ) ]
    fn score(&self, params: &Array1<f64>) -> Array1<f64> {
        let kvars = self.exog.ncols();
        let mut grad = Array1::zeros(kvars);
        for i in 0..self.endog.len() {
            let q_i = 2.0 * self.endog[i] - 1.0;
            let z = q_i * self.predict_linear(params, i);
            let ratio = (q_i * self.pdf(z)) / self.cdf(z);
            // multiply ratio * x_i
            let row = self.exog.row(i);
            for j in 0..kvars {
                grad[j] += ratio * row[j];
            }
        }
        grad
    }

    /// Hessian => -Σ [ λ_i (λ_i + x_i'β) x_i x_i' ]
    fn hessian(&self, params: &Array1<f64>) -> Array2<f64> {
        let kvars = self.exog.ncols();
        let mut hess = Array2::zeros((kvars, kvars));
        for i in 0..self.endog.len() {
            let q_i = 2.0 * self.endog[i] - 1.0;
            let xbeta = self.predict_linear(params, i);
            let z = q_i * xbeta;
            let cdf_ = self.cdf(z);
            let pdf_ = self.pdf(z);
            let lambda = (q_i * pdf_) / cdf_;
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
}

/// Naively invert matrix (k x k) with no pivoting (for demonstration).
fn invert_matrix_naive(mat: &Array2<f64>) -> Option<Array2<f64>> {
    let n = mat.nrows();
    if mat.ncols() != n {
        return None;
    }

    // Augment [mat|I]
    let mut aug = Array2::<f64>::zeros((n, 2*n));
    for r in 0..n {
        for c in 0..n {
            aug[[r, c]] = mat[[r, c]];
        }
        aug[[r, r + n]] = 1.0;
    }

    // Forward elim
    for i in 0..n {
        let pivot = aug[[i, i]];
        if pivot.abs() < 1e-14 {
            return None;
        }
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

    // Back substitution
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
            inv[[r, c]] = aug[[r, c+n]];
        }
    }
    Some(inv)
}

/// Multiply mat (k x k) by vec (k), returning a vec (k).
fn mat_vec_mul(mat: &Array2<f64>, vec: &Array1<f64>) -> Array1<f64> {
    let k = vec.len();
    let mut out = Array1::<f64>::zeros(k);
    for i in 0..k {
        let mut val = 0.0;
        for j in 0..k {
            val += mat[[i, j]] * vec[j];
        }
        out[i] = val;
    }
    out
}

/// Minimal results struct after fitting Probit
struct ProbitFitResults {
    params: Array1<f64>,
    loglike: f64,
    iterations: usize,
    converged: bool,
}

/// Fitting with naive Newton iteration
impl Probit {
    fn fit_naive_newton(&self, max_iter: usize, tol: f64) -> ProbitFitResults {
        let k = self.exog.ncols();
        let mut params = Array1::<f64>::zeros(k);
        let mut ll_old = self.loglike(&params);
        let mut converged = false;
        let mut iter_used = 0;

        for iter in 0..max_iter {
            iter_used = iter;
            let grad = self.score(&params);
            let hess = self.hessian(&params);
            let maybe_inv = invert_matrix_naive(&hess);
            if let Some(inv_hess) = maybe_inv {
                let step = mat_vec_mul(&inv_hess, &grad);
                // Newton update: β_{new} = β - step
                let new_params = &params - &step;
                let ll_new = self.loglike(&new_params);
                let diff = (ll_new - ll_old).abs();
                params = new_params;
                ll_old = ll_new;
                if diff < tol {
                    converged = true;
                    break;
                }
            } else {
                eprintln!("Hessian not invertible at iteration {}", iter);
                break;
            }
        }

        ProbitFitResults {
            params,
            loglike: ll_old,
            iterations: iter_used,
            converged,
        }
    }
}

/// Expose a `fit_probit` function to Python, demonstrating how you can
/// fit your own Probit in Rust. (Naive approach, no partial pivot.)
#[pyfunction]
fn fit_probit<'py>(
    py: Python<'py>,
    endog_py: &PyArray1<f64>,
    exog_py: &PyArray2<f64>,
    max_iter: Option<usize>,
    tol: Option<f64>,
) -> PyResult<&'py PyDict> {
    let endog = unsafe { endog_py.as_array() }.to_owned();
    let exog = unsafe { exog_py.as_array() }.to_owned();

    // Build the Probit, fit with naive Newton
    let model = Probit::new(endog, exog);
    let max_iter = max_iter.unwrap_or(50);
    let tol = tol.unwrap_or(1e-8);

    let results = model.fit_naive_newton(max_iter, tol);

    // Return a dictionary with final params, loglike, iteration count, etc.
    let out = PyDict::new(py);
    // Convert params => Python list
    let params_list: Vec<f64> = results.params.to_vec();
    out.set_item("params", params_list)?;
    out.set_item("loglike", results.loglike)?;
    out.set_item("iterations", results.iterations)?;
    out.set_item("converged", results.converged)?;

    Ok(out)
}

/// A Python module implemented in Rust.
#[pymodule]
fn rustats(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(ame, m)?)?;
    // New Probit "fit_probit" function
    m.add_function(wrap_pyfunction!(fit_probit, m)?)?;
    Ok(())
}
