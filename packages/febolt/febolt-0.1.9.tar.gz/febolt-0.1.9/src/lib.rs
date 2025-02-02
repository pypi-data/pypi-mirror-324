// src/lib.rs

use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use pyo3::types::{PyAny, PyDict};
use numpy::{IntoPyArray, PyArray1, PyArray2};
use ndarray::{Array1, Array2, Axis, ArrayView1, ArrayView2};
use statrs::distribution::{Continuous, ContinuousCDF, Normal};
use std::collections::HashMap;
use std::fmt::Write as _;

// Bring in ndarray-linalg traits for solving linear systems and inversion.
use ndarray_linalg::{Solve, Inverse};

//------------------------------------------------------------------------------
// Minimal Probit
//------------------------------------------------------------------------------
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
        // avoid extreme tails
        let c = self.normal.cdf(x);
        c.max(1e-15).min(1.0 - 1e-15)
    }

    fn pdf(&self, x: f64) -> f64 {
        self.normal.pdf(x)
    }

    /// Compute x_i' * beta
    fn xbeta(&self, params: &Array1<f64>, i: usize) -> f64 {
        self.exog.row(i).dot(params)
    }

    /// Compute the log likelihood: sum ln( Phi(q_i * x_i'beta) ), where q_i = 2*y_i - 1
    fn loglike(&self, params: &Array1<f64>) -> f64 {
        self.endog
            .iter()
            .enumerate()
            .map(|(i, &y)| {
                let q = 2.0 * y - 1.0;
                let z = q * self.xbeta(params, i);
                self.cdf(z).ln()
            })
            .sum()
    }

    /// Compute the score (gradient)
    fn score(&self, params: &Array1<f64>) -> Array1<f64> {
        let kvars = self.exog.ncols();
        let mut grad = Array1::<f64>::zeros(kvars);
        for i in 0..self.endog.len() {
            let q = 2.0 * self.endog[i] - 1.0;
            let z = q * self.xbeta(params, i);
            let ratio = (q * self.pdf(z)) / self.cdf(z);
            grad += &(self.exog.row(i).to_owned() * ratio);
        }
        grad
    }

    /// Compute the Hessian (observed information matrix)
    fn hessian(&self, params: &Array1<f64>) -> Array2<f64> {
        let kvars = self.exog.ncols();
        let mut hess = Array2::<f64>::zeros((kvars, kvars));
        for i in 0..self.endog.len() {
            let q = 2.0 * self.endog[i] - 1.0;
            let xbeta = self.xbeta(params, i);
            let z = q * xbeta;
            let cdf_ = self.cdf(z);
            let pdf_ = self.pdf(z);
            let lam = (q * pdf_) / cdf_;
            let val = lam * (lam + xbeta);
            let row = self.exog.row(i);
            hess -= &(&row.to_owned().insert_axis(Axis(1))
                .dot(&row.to_owned().insert_axis(Axis(0)))
                * val);
        }
        hess
    }

    /// Fit via (naive) Newton–Raphson. Instead of computing an explicit inverse, we solve the linear system.
    fn fit_naive_newton(&self, max_iter: usize, tol: f64) -> (Array1<f64>, f64, bool, usize) {
        let k = self.exog.ncols();
        let mut params = Array1::<f64>::zeros(k);
        let mut ll_old = self.loglike(&params);
        let mut conv = false;
        let mut iter_used = 0;
        for iter in 0..max_iter {
            iter_used = iter;
            let grad = self.score(&params);
            let hess = self.hessian(&params);
            let step = match hess.solve(&grad) {
                Ok(sol) => sol,
                Err(_) => {
                    eprintln!("Hessian near singular at iteration {}", iter);
                    break;
                }
            };
            let new_params = &params - &step;
            let ll_new = self.loglike(&new_params);
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
// White & Cluster: robust covariance functions
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
// RustProbitModel => sub-struct with exog, endog, exog_names
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
// RustProbitResults => contains .params, .model, .cov_params(), etc.
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
// Main fit_probit function with defaults, auto-flatten, robust, cluster
//------------------------------------------------------------------------------
#[pyfunction]
#[allow(clippy::too_many_arguments)]
fn fit_probit(
    py: Python<'_>,
    endog_py: &PyAny,   // user might pass shape (nobs,1) or (nobs,)
    exog_py: &PyArray2<f64>,
    max_iter: Option<usize>,
    tol: Option<f64>,
    robust: Option<bool>,
    cluster_vars: Option<&PyAny>,
) -> PyResult<RustProbitResults> {
    // 1) Flatten endog if shape=(nobs,1) => shape=(nobs,)
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
            (r, Some(c)) => {
                return Err(pyo3::exceptions::PyValueError::new_err(
                    format!("endog must be shape (nobs,) or (nobs,1). Got shape=({},{})", r, c)
                ));
            }
        }
    };

    // 2) exog is 2D
    let exog: Array2<f64> = unsafe { exog_py.as_array() }.to_owned();

    // defaults
    let max_iter = max_iter.unwrap_or(35);
    let tol = tol.unwrap_or(1e-6);
    let do_robust = robust.unwrap_or(false);

    // 3) Fit
    let model_data = Probit::new(endog.clone(), exog.clone());
    let (params, llf, converged, iterations) = model_data.fit_naive_newton(max_iter, tol);

    // 4) Classical covariance: cov = -H^-1.
    let hess_final = model_data.hessian(&params);
    let cov_final = match hess_final.inv() {
        Ok(inv_hess) => -inv_hess,
        Err(_) => {
            eprintln!("Hessian singular => using identity for Cov");
            -Array2::<f64>::eye(exog.ncols())
        }
    };
    let mut cov_final = cov_final;

    // 5) Robust or cluster covariance adjustments
    if do_robust {
        let nobs = endog.len();
        let kvars = exog.ncols();
        let mut s_obs_mat = Array2::<f64>::zeros((nobs, kvars));
        for i in 0..nobs {
            let q = 2.0 * endog[i] - 1.0;
            let z = q * model_data.xbeta(&params, i);
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

        // Compute robust covariance:
        let h_inv = cov_final.mapv(|x| -x);
        cov_final = h_inv.dot(&final_mat).dot(&h_inv);
    }

    // 6) Convert results to Py objects
    let params_py = params.into_pyarray(py).to_owned();
    let cov_py = cov_final.into_pyarray(py).to_owned();
    let exog_py_ = exog.into_pyarray(py).to_owned();
    let endog_py_ = endog.into_pyarray(py).to_owned();

    // Use as_ref(py) to access the shape.
    let exog_array = exog_py_.as_ref(py);
    let shape = exog_array.shape();
    let mut exog_names = Vec::with_capacity(shape[1]);
    for j in 0..shape[1] {
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
        iterations_: iterations,
        converged_: converged,
    };

    Ok(result)
}

//------------------------------------------------------------------------------
// Helper functions for the AME function
//------------------------------------------------------------------------------

/// Add significance stars based on the p-value.
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

/// Downcast a Python object to NumPy PyArray2<f64> and get an ArrayView2<f64>.
fn as_array2_f64<'py>(obj: &'py PyAny) -> PyResult<ArrayView2<'py, f64>> {
    let pyarray = obj.downcast::<PyArray2<f64>>()?;
    // Unsafe conversion to ndarray view
    Ok(unsafe { pyarray.as_array() })
}

/// Downcast a Python object to NumPy PyArray1<f64> and get an ArrayView1<f64>.
fn as_array1_f64<'py>(obj: &'py PyAny) -> PyResult<ArrayView1<'py, f64>> {
    let pyarray = obj.downcast::<PyArray1<f64>>()?;
    Ok(unsafe { pyarray.as_array() })
}

/// Extracts (beta, cov_beta, exog_names, X) from the Python Probit model.
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
// AME function
//------------------------------------------------------------------------------
#[pyfunction]
fn ame<'py>(
    py: Python<'py>,
    probit_model: &'py PyAny,  // Our Python Probit model
    chunk_size: Option<usize>, // Optional chunk size for processing
) -> PyResult<&'py PyAny> {
    // STEP 1: Get Model Ingredients
    let params_pyarray: &PyArray1<f64> = probit_model.getattr("params")?.downcast()?;
    let beta = unsafe { params_pyarray.as_array() };
    let cov_pyarray: &PyArray2<f64> = probit_model.call_method0("cov_params")?.downcast()?;
    let cov_beta = unsafe { cov_pyarray.as_array() };
    let exog_names: Vec<String> = probit_model
        .getattr("model")?
        .getattr("exog_names")?
        .extract()?;
    let x_pyarray: &PyArray2<f64> = probit_model.getattr("model")?.getattr("exog")?.downcast()?;
    let X = unsafe { x_pyarray.as_array() };

    let (n, k) = (X.nrows(), X.ncols());
    let chunk = chunk_size.unwrap_or(n);

    // STEP 2: Identify Special Columns
    let intercept_indices: Vec<usize> = exog_names
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

    let is_discrete: Vec<usize> = exog_names
        .iter()
        .enumerate()
        .filter_map(|(j, _)| {
            if intercept_indices.contains(&j) {
                None
            } else if X.column(j).iter().all(|&v| v == 0.0 || v == 1.0) {
                Some(j)
            } else {
                None
            }
        })
        .collect();

    // STEP 3: Setup Calculation Tools
    let mut sum_ame = vec![0.0; k];
    let mut partial_jl_sums = vec![0.0; k * k];
    let normal = Normal::new(0.0, 1.0).unwrap();

    // STEP 4: Process Data in Chunks
    let mut idx_start = 0;
    while idx_start < n {
        let idx_end = (idx_start + chunk).min(n);
        let x_chunk = X.slice(ndarray::s![idx_start..idx_end, ..]);
        let z_chunk = x_chunk.dot(&beta);
        let phi_vals = z_chunk.mapv(|z| normal.pdf(z));

        // Process discrete features
        for &j in &is_discrete {
            let xj_col = x_chunk.column(j);
            let beta_j = beta[j];
            let delta_j1 = (1.0 - &xj_col).mapv(|x| x * beta_j);
            let delta_j0 = xj_col.mapv(|x| -x * beta_j);
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

        // Process continuous features
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

    // STEP 5: Final Calculations
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

    // STEP 6: Prepare Results
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

    // STEP 7: Create Pandas DataFrame
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
// PyO3 module
//------------------------------------------------------------------------------
#[pymodule]
fn febolt(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(fit_probit, m)?)?;
    m.add_function(wrap_pyfunction!(ame, m)?)?;
    Ok(())
}
