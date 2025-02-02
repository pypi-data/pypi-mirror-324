// src/lib.rs

use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use pyo3::types::{PyAny, PyDict};
use numpy::{IntoPyArray, PyArray1, PyArray2, PyReadonlyArray1, PyReadonlyArray2};
use ndarray::{Array1, Array2, Axis, ArrayView1, ArrayView2};
use statrs::distribution::{Continuous, ContinuousCDF, Normal};
use std::f64::consts::{PI, SQRT_2};
use std::collections::HashMap;
use std::fmt::Write as _;

// Bring in ndarray-linalg traits for solving linear systems and inversion.
use ndarray_linalg::{Solve, Inverse};

// Custom error function approximation
fn erf(x: f64) -> f64 {
    // Abramowitz and Stegun approximation (max error ~1.5e-7)
    let a1 = 0.254829592;
    let a2 = -0.284496736;
    let a3 = 1.421413741;
    let a4 = -1.453152027;
    let a5 = 1.061405429;
    let p = 0.3275911;

    let sign = if x < 0.0 { -1.0 } else { 1.0 };
    let x = x.abs();

    let t = 1.0 / (1.0 + p * x);
    let y = 1.0 - (((((a5 * t + a4) * t + a3) * t + a2) * t + a1) * t * (-x * x).exp());

    sign * y
}

struct Probit {
    endog: Array1<f64>,
    exog: Array2<f64>,
}

impl Probit {
    fn new(endog: Array1<f64>, exog: Array2<f64>) -> Self {
        Probit { endog, exog }
    }

    #[inline]
    fn cdf(&self, x: f64) -> f64 {
        let c = 0.5 * (1.0 + erf(x / SQRT_2));
        c.max(1e-15).min(1.0 - 1e-15)
    }

    #[inline]
    fn pdf(&self, x: f64) -> f64 {
        (-0.5 * x.powi(2)).exp() / (2.0 * PI).sqrt()
    }

    /// Compute the full linear predictor vector Xβ.
    fn xbeta_vec(&self, params: &Array1<f64>) -> Array1<f64> {
        self.exog.dot(params)
    }

    /// Compute the log likelihood without intermediate arrays.
    fn loglike_with_xbeta(&self, xbeta: &Array1<f64>) -> f64 {
        self.endog.iter()
            .zip(xbeta.iter())
            .map(|(y, xb)| {
                let q = 2.0 * y - 1.0;
                let z = q * xb;
                self.cdf(z).ln()
            })
            .sum()
    }

    /// Compute the score using direct accumulation.
    fn score_with_xbeta(&self, xbeta: &Array1<f64>) -> Array1<f64> {
        let mut grad = Array1::zeros(self.exog.ncols());
        for (i, (y, xb)) in self.endog.iter().zip(xbeta.iter()).enumerate() {
            let q_i = 2.0 * y - 1.0;
            let z_i = q_i * xb;
            let ratio = q_i * self.pdf(z_i) / self.cdf(z_i);
            self.exog.row(i).iter().zip(grad.iter_mut()).for_each(|(x, g)| *g += x * ratio);
        }
        grad
    }

    /// Compute the Hessian using direct accumulation.
    fn hessian_with_xbeta(&self, xbeta: &Array1<f64>) -> Array2<f64> {
        let k = self.exog.ncols();
        let mut hess = Array2::zeros((k, k));
        for (i, (y, xb)) in self.endog.iter().zip(xbeta.iter()).enumerate() {
            let q_i = 2.0 * y - 1.0;
            let z_i = q_i * xb;
            let pdf = self.pdf(z_i);
            let cdf = self.cdf(z_i);
            let lam = q_i * pdf / cdf;
            let val = lam * (lam + xb);
            
            let row = self.exog.row(i);
            for j in 0..k {
                let xj = row[j];
                for l in 0..k {
                    hess[(j, l)] -= xj * row[l] * val;
                }
            }
        }
        hess
    }

    /// Fit using precomputed xbeta to avoid redundant calculations.
fn fit_naive_newton(&self, max_iter: usize, tol: f64) -> (Array1<f64>, f64, bool, usize) {
    let k = self.exog.ncols();
    let mut params = Array1::zeros(k);
    let mut conv = false;
    let mut iter_used = 0;
    
    // Compute initial xbeta and log likelihood
    let xbeta_initial = self.xbeta_vec(&params);
    let mut ll_old = self.loglike_with_xbeta(&xbeta_initial);

    for iter in 0..max_iter {
        iter_used = iter;
        let xbeta = self.xbeta_vec(&params);
        
        let grad = self.score_with_xbeta(&xbeta);
        let hess = self.hessian_with_xbeta(&xbeta);

        let step = match hess.solve(&grad) {
            Ok(sol) => sol,
            Err(_) => {
                eprintln!("Hessian singular at iteration {}", iter);
                break;
            }
        };

        let new_params = &params - &step;
        let xbeta_new = self.xbeta_vec(&new_params);
        let ll_new = self.loglike_with_xbeta(&xbeta_new);

        if (ll_new - ll_old).abs() < tol {
            params = new_params;
            ll_old = ll_new;
            conv = true;
            break;
        }
        params = new_params;
        ll_old = ll_new;
    }
    (params, ll_old, conv, iter_used)
}
}

//------------------------------------------------------------------------------
// White & Cluster Robust Covariance Functions
//------------------------------------------------------------------------------
fn calc_white_crossprod(s_obs: &Array2<f64>) -> Array2<f64> {
    s_obs.t().dot(s_obs)
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


//------------------------------------------------------------------------------
// RustProbitModel: Holds the input data and variable names
//------------------------------------------------------------------------------
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


//------------------------------------------------------------------------------
// RustProbitResults: Stores the estimation results and model reference
//------------------------------------------------------------------------------
#[pyclass]
struct RustProbitResults {
    params_: Py<PyArray1<f64>>,
    cov_: Py<PyArray2<f64>>,
    model_: RustProbitModel,
    loglike_: f64,
    iterations_: usize,
    converged_: bool,
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
        self.iterations_
    }

    #[getter]
    fn converged(&self) -> bool {
        self.converged_
    }
}


//------------------------------------------------------------------------------
// Main fit_probit function using PyReadonlyArray for input data.
//------------------------------------------------------------------------------
#[pyfunction]
#[allow(clippy::too_many_arguments)]
fn fit_probit(
    py: Python<'_>,
    endog_py: PyReadonlyArray1<f64>,
    exog_py: PyReadonlyArray2<f64>,
    max_iter: Option<usize>,
    tol: Option<f64>,
    robust: Option<bool>,
    cluster_vars: Option<&PyAny>,
) -> PyResult<RustProbitResults> {
    // Get read-only views of the input arrays.
    let endog_view = endog_py.as_array();
    let exog_view = exog_py.as_array();

    // If needed, clone the arrays to get an owned copy.
    let endog = endog_view.to_owned();
    let exog = exog_view.to_owned();

    // defaults
    let max_iter = max_iter.unwrap_or(35);
    let tol = tol.unwrap_or(1e-6);
    let do_robust = robust.unwrap_or(false);

    // Fit the model.
    let model_data = Probit::new(endog.clone(), exog.clone());
    let (params, llf, converged, iterations) = model_data.fit_naive_newton(max_iter, tol);

    // Compute final xbeta for covariance calculations
    let xbeta_final = model_data.xbeta_vec(&params);

    // Classical covariance: cov = -H^-1
    let hess_final = model_data.hessian_with_xbeta(&xbeta_final);
    let cov_final = match hess_final.inv() {
        Ok(inv_hess) => -inv_hess,
        Err(_) => {
            eprintln!("Hessian singular => using identity for Cov");
            -Array2::<f64>::eye(exog.ncols())
        }
    };
    let mut cov_final = cov_final;

    // Robust or cluster covariance adjustments
    if do_robust {
        let nobs = endog.len();
        let kvars = exog.ncols();
        let mut s_obs_mat = Array2::<f64>::zeros((nobs, kvars));

        // Precompute all z values and ratios
        for i in 0..nobs {
            let q = 2.0 * endog[i] - 1.0;
            let z = q * xbeta_final[i];  // Use precomputed xbeta
            let ratio = (q * model_data.pdf(z)) / model_data.cdf(z);
            s_obs_mat.row_mut(i).assign(&(&exog.row(i) * ratio));
        }
        let final_mat = if let Some(obj) = cluster_vars {
            if obj.is_none() {
                calc_white_crossprod(&s_obs_mat)
            } else {
                let arr_2d = obj.downcast::<PyArray2<f64>>()?;
                let cluster_view = unsafe { arr_2d.as_array() }.to_owned();
                if cluster_view.nrows() != nobs {
                    return Err(pyo3::exceptions::PyValueError::new_err(
                        format!("cluster shape mismatch. got {} rows, nobs={}", cluster_view.nrows(), nobs)
                    ));
                }
                let keys = combine_cluster_keys(&cluster_view);
                let mut group_sums: HashMap<String, Array1<f64>> = HashMap::new();
                for (i, key) in keys.iter().enumerate() {
                    group_sums
                        .entry(key.clone())
                        .and_modify(|v| *v += &s_obs_mat.row(i))
                        .or_insert(s_obs_mat.row(i).to_owned());
                }
                let mut M = Array2::<f64>::zeros((kvars, kvars));
                for (_, sumv) in group_sums {
                    M += &sumv.view().insert_axis(Axis(1))
                        .dot(&sumv.view().insert_axis(Axis(0)));
                }
                M
            }
        } else {
            calc_white_crossprod(&s_obs_mat)
        };

        // Compute robust covariance: cov_robust = H_inv * M * H_inv.
        let h_inv = cov_final.mapv(|x| -x);
        cov_final = h_inv.dot(&final_mat).dot(&h_inv);
    }

    // Convert results to Python objects.
    let params_py = params.into_pyarray(py).to_owned();
    let cov_py = cov_final.into_pyarray(py).to_owned();
    let exog_py_owned = exog.into_pyarray(py).to_owned();
    let endog_py_owned = endog.into_pyarray(py).to_owned();

    // Auto-generate exog names.
    let exog_array = exog_py_owned.as_ref(py);
    let shape = exog_array.shape();
    let mut exog_names = Vec::with_capacity(shape[1]);
    for j in 0..shape[1] {
        exog_names.push(format!("x{}", j));
    }

    let rust_model = RustProbitModel {
        exog_: exog_py_owned,
        endog_: endog_py_owned,
        exog_names_: exog_names,
    };

    let result = RustProbitResults {
        params_: params_py,
        cov_: cov_py,
        model_: rust_model,
        loglike_: llf,
        iterations_: iterations,
        converged_: converged,
    };

    Ok(result)
}


//------------------------------------------------------------------------------
// Helper functions for the AME function
//------------------------------------------------------------------------------
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

fn as_array2_f64<'py>(obj: &'py PyAny) -> PyResult<ArrayView2<'py, f64>> {
    let pyarray = obj.downcast::<PyArray2<f64>>()?;
    Ok(unsafe { pyarray.as_array() })
}

fn as_array1_f64<'py>(obj: &'py PyAny) -> PyResult<ArrayView1<'py, f64>> {
    let pyarray = obj.downcast::<PyArray1<f64>>()?;
    Ok(unsafe { pyarray.as_array() })
}

fn extract_probit_model_components<'py>(
    _py: Python<'py>,
    probit_model: &'py PyAny,
) -> PyResult<(Array1<f64>, Array2<f64>, Vec<String>, Array2<f64>)> {
    let params_obj = probit_model.getattr("params")?;
    let beta_view = as_array1_f64(params_obj)?;
    let beta = beta_view.to_owned();

    let cov_obj = probit_model.call_method0("cov_params")?;
    let cov_view = as_array2_f64(cov_obj)?;
    let cov_beta = cov_view.to_owned();

    let exog_names_py: Vec<String> = probit_model
        .getattr("model")?
        .getattr("exog_names")?
        .extract()?;

    let x_obj = probit_model.getattr("model")?.getattr("exog")?;
    let x_view = as_array2_f64(x_obj)?;
    let X = x_view.to_owned();

    Ok((beta, cov_beta, exog_names_py, X))
}


//------------------------------------------------------------------------------
// AME (Average Marginal Effects) function
//------------------------------------------------------------------------------
#[pyfunction]
fn ame<'py>(
    py: Python<'py>,
    probit_model: &'py PyAny,  // The Python Probit model
    chunk_size: Option<usize>, // Optional chunk size for processing
) -> PyResult<&'py PyAny> {
    // STEP 1: Get model ingredients.
    let params_pyarray: &PyArray1<f64> = probit_model.getattr("params")?.downcast()?;
    let beta = unsafe { params_pyarray.as_array() };
    let cov_pyarray: &PyArray2<f64> = probit_model.call_method0("cov_params")?.downcast()?;
    let cov_beta = unsafe { cov_pyarray.as_array() };
    let mut exog_names: Vec<String> = probit_model
        .getattr("model")?
        .getattr("exog_names")?
        .extract()?;
    let x_pyarray: &PyArray2<f64> = probit_model.getattr("model")?.getattr("exog")?.downcast()?;
    let X = unsafe { x_pyarray.as_array() };

    let (n, k) = (X.nrows(), X.ncols());
    let chunk = chunk_size.unwrap_or(n);

    // STEP 2: Identify intercept columns (by name and auto-detection).
    let mut intercept_indices: Vec<usize> = exog_names
        .iter()
        .enumerate()
        .filter_map(|(i, nm)| {
            let ln = nm.to_lowercase();
            if ln == "const" || ln == "intercept" {
                Some(i)
            } else {
                None
            }
        })
        .collect();
    for j in 0..k {
        if X.column(j).iter().all(|&v| (v - X[(0, j)]).abs() < 1e-8) {
            if !intercept_indices.contains(&j) {
                intercept_indices.push(j);
                exog_names[j] = "Intercept".to_string();
            }
        }
    }

    // Identify discrete variables (excluding intercepts).
    let is_discrete: Vec<usize> = (0..k)
        .filter(|&j| {
            if intercept_indices.contains(&j) {
                false
            } else {
                X.column(j).iter().all(|&v| v == 0.0 || v == 1.0)
            }
        })
        .collect();

    // STEP 3: Setup calculation tools.
    let mut sum_ame = vec![0.0; k];
    let mut partial_jl_sums = vec![0.0; k * k];
    let normal = Normal::new(0.0, 1.0).unwrap();

    // STEP 4: Process data in chunks.
    let mut idx_start = 0;
    while idx_start < n {
        let idx_end = (idx_start + chunk).min(n);
        let x_chunk = X.slice(ndarray::s![idx_start..idx_end, ..]);
        let z_chunk = x_chunk.dot(&beta);
        let phi_vals = z_chunk.mapv(|z| normal.pdf(z));

        // Process discrete features.
        for &j in &is_discrete {
            let xj_col = x_chunk.column(j);
            let beta_j = beta[j];
            let delta_j1 = xj_col.mapv(|x| if x == 0.0 { beta_j } else { 0.0 });
            let delta_j0 = xj_col.mapv(|x| if x == 1.0 { -beta_j } else { 0.0 });
            let z_j1 = &z_chunk + &delta_j1;
            let z_j0 = &z_chunk + &delta_j0;
            let cdf_diff_sum = z_j1.mapv(|z| normal.cdf(z)).sum()
                - z_j0.mapv(|z| normal.cdf(z)).sum();
            sum_ame[j] += cdf_diff_sum;

            let pdf_j1 = z_j1.mapv(|z| normal.pdf(z));
            let pdf_j0 = z_j0.mapv(|z| normal.pdf(z));
            for l in 0..k {
                let xl_col = x_chunk.column(l);
                let grad = if l == j {
                    pdf_j1.sum()
                } else {
                    (&pdf_j1 - &pdf_j0).dot(&xl_col)
                };
                partial_jl_sums[j * k + l] += grad;
            }
        }

        // Process continuous features (non-intercept and non-discrete).
        for j in 0..k {
            if intercept_indices.contains(&j) || is_discrete.contains(&j) {
                continue;
            }
            let beta_j = beta[j];
            sum_ame[j] += beta_j * phi_vals.sum();
            for l in 0..k {
                let grad = if j == l {
                    phi_vals.sum()
                } else {
                    -beta_j * (&z_chunk * &x_chunk.column(l)).dot(&phi_vals)
                };
                partial_jl_sums[j * k + l] += grad;
            }
        }
        idx_start = idx_end;
    }

    // STEP 5: Final calculations.
    let ame: Vec<f64> = sum_ame.iter().map(|v| v / n as f64).collect();
    let mut grad_ame = Array2::zeros((k, k));
    for j in 0..k {
        for l in 0..k {
            grad_ame[(j, l)] = partial_jl_sums[j * k + l] / n as f64;
        }
    }
    let cov_ame = grad_ame.dot(&cov_beta).dot(&grad_ame.t());
    let var_ame: Vec<f64> = cov_ame.diag().iter().map(|&v| v.max(0.0)).collect();
    let se_ame: Vec<f64> = var_ame.iter().map(|v| v.sqrt()).collect();

    // STEP 6: Prepare output, skipping intercept columns.
    let (mut dy_dx, mut se_err, mut z_vals, mut p_vals, mut sig, mut names) =
        (Vec::new(), Vec::new(), Vec::new(), Vec::new(), Vec::new(), Vec::new());
    for j in 0..k {
        if intercept_indices.contains(&j) {
            continue;
        }
        dy_dx.push(ame[j]);
        se_err.push(se_ame[j]);
        let z = if se_ame[j] > 0.0 {
            ame[j] / se_ame[j]
        } else {
            f64::NAN
        };
        z_vals.push(z);
        let p = 2.0 * (1.0 - normal.cdf(z.abs()));
        p_vals.push(p);
        sig.push(add_significance_stars(p));
        names.push(exog_names[j].clone());
    }

    // STEP 7: Create a Pandas DataFrame for output.
    let pd = py.import("pandas")?;
    let data = PyDict::new(py);
    data.set_item("dy/dx", dy_dx)?;
    data.set_item("Std. Err", se_err)?;
    data.set_item("z", z_vals)?;
    data.set_item("Pr(>|z|)", p_vals)?;
    data.set_item("Significance", sig)?;

    let kwargs = PyDict::new(py);
    kwargs.set_item("data", data)?;
    kwargs.set_item("index", names)?;

    pd.call_method("DataFrame", (), Some(kwargs))
}


//------------------------------------------------------------------------------
// PyO3 Module Definition
//------------------------------------------------------------------------------
#[pymodule]
fn febolt(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(fit_probit, m)?)?;
    m.add_function(wrap_pyfunction!(ame, m)?)?;
    Ok(())
}
