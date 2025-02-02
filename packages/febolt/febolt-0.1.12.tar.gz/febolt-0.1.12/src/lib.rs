// src/lib.rs

use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use pyo3::types::{PyAny, PyDict};
use numpy::{IntoPyArray, PyArray1, PyArray2, PyReadonlyArray1, PyReadonlyArray2, PyReadonlyArrayDyn};
use ndarray::{Array1, Array2, Axis, ArrayView1, ArrayView2};
use statrs::distribution::{Continuous, ContinuousCDF, Normal};
use std::f64::consts::{PI, SQRT_2};
use std::collections::HashMap;
use std::hash::{Hash, Hasher};
use std::fmt::Write as _;

// Bring in ndarray-linalg traits for solving linear systems and inversion.
use ndarray_linalg::{Solve, Inverse};

/// Custom error function approximation using Abramowitz and Stegun (max error ~1.5e-7)
fn erf(x: f64) -> f64 {
    let a1 = 0.254829592;
    let a2 = -0.284496736;
    let a3 = 1.421413741;
    let a4 = -1.453152027;
    let a5 = 1.061405429;
    let p = 0.3275911;

    let sign = if x < 0.0 { -1.0 } else { 1.0 };
    let x = x.abs();

    let t = 1.0 / (1.0 + p * x);
    let y = 1.0 - ((((a5 * t + a4) * t + a3) * t + a2) * t + a1) * t * (-x * x).exp();
    sign * y
}

/// The Probit model holds views to the endogenous and exogenous data.
struct Probit<'a> {
    endog: ArrayView1<'a, f64>,
    exog: ArrayView2<'a, f64>,
}

impl<'a> Probit<'a> {
    fn new(endog: ArrayView1<'a, f64>, exog: ArrayView2<'a, f64>) -> Self {
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

    /// Compute the linear predictor: xbeta = exog * params.
    /// (Reuses the output buffer.)
    fn xbeta(&self, params: &ArrayView1<f64>, out: &mut Array1<f64>) {
        *out = self.exog.dot(params);
    }

    /// Compute the log-likelihood in a vectorized manner.
    fn loglike(&self, xbeta: &ArrayView1<f64>) -> f64 {
        let q = self.endog.mapv(|y| 2.0 * y - 1.0);
        let z = &q * xbeta;
        z.mapv(|zi| self.cdf(zi).ln()).sum()
    }

    /// Compute the score (gradient) using vectorized operations.
    fn score(&self, xbeta: &ArrayView1<f64>, grad: &mut Array1<f64>) {
        let q = self.endog.mapv(|y| 2.0 * y - 1.0);
        let z = &q * xbeta;
        let ratio = z.mapv(|zi| {
            let pdf_val = self.pdf(zi);
            let cdf_val = self.cdf(zi);
            pdf_val / cdf_val
        });
        let adjusted = &q * &ratio;
        *grad = self.exog.t().dot(&adjusted);
    }

    /// Compute the Hessian as -X' W X, where W is a diagonal weight matrix.
    fn hessian(&self, xbeta: &ArrayView1<f64>, hess: &mut Array2<f64>) {
        let q = self.endog.mapv(|y| 2.0 * y - 1.0);
        let z = &q * xbeta;
        let pdfs = z.mapv(|zi| self.pdf(zi));
        let cdfs = z.mapv(|zi| self.cdf(zi));
        let ratio = pdfs / cdfs;
        // Per-observation weight: w_i = (ratio)^2 + ratio * z.
        let weights: Array1<f64> = z.iter().zip(ratio.iter())
            .map(|(&zi, &r)| (r * r + r * zi).max(0.0))
            .collect();

        // Build a weighted version of exog (each row multiplied by sqrt(weight)).
        let mut weighted_exog = self.exog.to_owned();
        for (i, &w) in weights.iter().enumerate() {
            let scale = w.sqrt();
            weighted_exog.row_mut(i).mapv_inplace(|x| x * scale);
        }
        // Compute hess = - (weighted_exog.t() dot weighted_exog)
        *hess = -weighted_exog.t().dot(&weighted_exog);
    }

    /// Naive Newton–Raphson optimizer for Probit estimation.
    fn fit_naive_newton(&self, max_iter: usize, tol: f64) -> (Array1<f64>, f64, bool, usize) {
        let k = self.exog.ncols();
        let mut params = Array1::zeros(k);
        let mut xbeta = Array1::zeros(self.exog.nrows());
        let mut grad = Array1::zeros(k);
        let mut hess = Array2::zeros((k, k));
        let mut ll_old: f64;
        let mut conv = false;
        let mut iter_used = 0;

        self.xbeta(&params.view(), &mut xbeta);
        ll_old = self.loglike(&xbeta.view());

        for iter in 0..max_iter {
            iter_used = iter;
            self.score(&xbeta.view(), &mut grad);
            self.hessian(&xbeta.view(), &mut hess);

            let step = match hess.solve(&grad) {
                Ok(s) => s,
                Err(_) => {
                    eprintln!("Hessian singular at iteration {}", iter);
                    break;
                }
            };

            params.scaled_add(-1.0, &step);
            self.xbeta(&params.view(), &mut xbeta);
            let ll_new = self.loglike(&xbeta.view());

            if (ll_new - ll_old).abs() < tol {
                conv = true;
                ll_old = ll_new;
                break;
            }
            ll_old = ll_new;
        }
        (params, ll_old, conv, iter_used)
    }
}

/// Compute the robust covariance using a “meat” matrix.
/// 
/// This version reuses a temporary score buffer (avoiding per-iteration allocations)
/// and uses views where possible. If a cluster variable is provided (assumed to be a
/// single-column array), observations are grouped by cluster using a HashMap.
fn robust_covariance(
    exog: &ArrayView2<f64>,
    xbeta: &ArrayView1<f64>,
    endog: &ArrayView1<f64>,
    h_inv: &ArrayView2<f64>,
    cluster: Option<ArrayView2<f64>>,
) -> Array2<f64> {
    let nobs = exog.nrows();
    let kvars = exog.ncols();
    let mut M = Array2::<f64>::zeros((kvars, kvars));
    let mut score = Array1::<f64>::zeros(kvars);

    if let Some(cluster) = cluster {
        if cluster.ncols() != 1 {
            eprintln!("Cluster variable expected to have one column; got {}", cluster.ncols());
            // Fall back to White’s estimator without clustering.
            for i in 0..nobs {
                let q = 2.0 * endog[i] - 1.0;
                let z = q * xbeta[i];
                let pdf = (-0.5 * z.powi(2)).exp() / (2.0 * PI).sqrt();
                let cdf = (0.5 * (1.0 + erf(z / SQRT_2))).max(1e-15).min(1.0 - 1e-15);
                let ratio = q * pdf / cdf;
                score.assign(&exog.row(i));
                score.mapv_inplace(|x| x * ratio);
                M = &M + &score.view().insert_axis(Axis(1)).dot(&score.view().insert_axis(Axis(0)));
            }
        } else {
            let mut cluster_map: HashMap<u64, Array1<f64>> = HashMap::new();
            for i in 0..nobs {
                let cl_val = cluster[[i, 0]];
                let key = cl_val.to_bits();
                let q = 2.0 * endog[i] - 1.0;
                let z = q * xbeta[i];
                let pdf = (-0.5 * z.powi(2)).exp() / (2.0 * PI).sqrt();
                let cdf = (0.5 * (1.0 + erf(z / SQRT_2))).max(1e-15).min(1.0 - 1e-15);
                let ratio = q * pdf / cdf;
                score.assign(&exog.row(i));
                score.mapv_inplace(|x| x * ratio);
                cluster_map
                    .entry(key)
                    .and_modify(|v| *v += &score)
                    .or_insert(score.clone());
            }
            for (_key, score_sum) in cluster_map {
                M = &M + &score_sum.view().insert_axis(Axis(1)).dot(&score_sum.view().insert_axis(Axis(0)));
            }
        }
    } else {
        // White's estimator: sum outer products for each observation.
        for i in 0..nobs {
            let q = 2.0 * endog[i] - 1.0;
            let z = q * xbeta[i];
            let pdf = (-0.5 * z.powi(2)).exp() / (2.0 * PI).sqrt();
            let cdf = (0.5 * (1.0 + erf(z / SQRT_2))).max(1e-15).min(1.0 - 1e-15);
            let ratio = q * pdf / cdf;
            score.assign(&exog.row(i));
            score.mapv_inplace(|x| x * ratio);
            M = &M + &score.view().insert_axis(Axis(1)).dot(&score.view().insert_axis(Axis(0)));
        }
    }

    // Final robust covariance: h_inv * M * h_inv.
    h_inv.dot(&M).dot(h_inv)
}

//
// Python-facing structures and functions
//

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
    iterations_: usize,
    converged_: bool,
}

#[pymethods]
impl RustProbitResults {
    #[getter]
    fn params(&self) -> Py<PyArray1<f64>> {
        self.params_.clone()
    }
    #[getter]
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

#[pyfunction]
#[allow(clippy::too_many_arguments)]
fn fit_probit(
    py: Python<'_>,
    endog_py: PyReadonlyArrayDyn<f64>,
    exog_py: PyReadonlyArray2<f64>,
    max_iter: Option<usize>,
    tol: Option<f64>,
    robust: Option<bool>,
    cluster_vars: Option<&PyAny>,
) -> PyResult<RustProbitResults> {
    // Get a view of the endogenous variable and flatten if needed.
    let endog_view = endog_py.as_array();
    let endog: ArrayView1<f64> = if endog_view.ndim() == 2 && endog_view.shape()[1] == 1 {
        endog_view.into_dimensionality::<ndarray::Ix1>().map_err(|_| {
            PyErr::new::<pyo3::exceptions::PyValueError, _>("Failed to flatten endog array with shape (N,1)")
        })?
    } else if endog_view.ndim() == 1 {
        endog_view.into_dimensionality::<ndarray::Ix1>().unwrap()
    } else {
        return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
            "endog must be 1-dimensional or 2-dimensional with shape (N,1)",
        ));
    };

    let exog = exog_py.as_array();

    // Create the Probit model instance.
    let probit = Probit::new(endog, exog);

    let max_iter = max_iter.unwrap_or(35);
    let tol = tol.unwrap_or(1e-6);
    let do_robust = robust.unwrap_or(false);

    // Fit the model.
    let (params, llf, converged, iterations) = probit.fit_naive_newton(max_iter, tol);

    // Reuse the xbeta buffer (pre-allocated) for subsequent covariance calculations.
    let mut xbeta = Array1::zeros(exog.nrows());
    probit.xbeta(&params.view(), &mut xbeta);

    // Compute the classical covariance as -H^{-1}.
    let mut hess = Array2::zeros((params.len(), params.len()));
    probit.hessian(&xbeta.view(), &mut hess);
    let mut cov_final = match hess.inv() {
        Ok(inv_hess) => -inv_hess,
        Err(_) => {
            eprintln!("Hessian singular => using identity for covariance");
            -Array2::<f64>::eye(exog.ncols())
        }
    };

    if do_robust {
        let cluster_view = if let Some(obj) = cluster_vars {
            let arr_2d = obj.downcast::<PyArray2<f64>>()?;
            let view = unsafe { arr_2d.as_array() };
            if view.nrows() != exog.nrows() {
                return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
                    format!("Cluster vars has {} rows, expected {}", view.nrows(), exog.nrows()),
                ));
            }
            Some(view)
        } else {
            None
        };

        // Use the inverse of the negative Hessian.
        let h_inv = cov_final.mapv(|x| -x);
        cov_final = robust_covariance(&exog.view(), &xbeta.view(), &endog, &h_inv.view(), cluster_view);
    }

    // Prepare Python arrays for output.
    let params_py = params.into_pyarray(py).to_owned();
    let cov_py = cov_final.into_pyarray(py).to_owned();
    let exog_py_owned = exog_py.to_owned_array().into_pyarray(py).to_owned();
    let endog_owned: Array1<f64> = endog.to_owned();
    let endog_py_owned = endog_owned.into_pyarray(py).to_owned();

    let exog_names = (0..exog.ncols()).map(|j| format!("x{}", j)).collect();

    Ok(RustProbitResults {
        params_: params_py,
        cov_: cov_py,
        model_: RustProbitModel {
            exog_: exog_py_owned,
            endog_: endog_py_owned,
            exog_names_: exog_names,
        },
        loglike_: llf,
        iterations_: iterations,
        converged_: converged,
    })
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
