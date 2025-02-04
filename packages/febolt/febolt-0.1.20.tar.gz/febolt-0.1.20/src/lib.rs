// src/lib.rs

use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use pyo3::types::{PyAny, PyDict};
use numpy::{PyArray1, PyArray2, PyReadonlyArray2, PyReadonlyArrayDyn};
use ndarray::{Array1, Array2, Axis, ArrayView1, ArrayView2};
use std::f32::consts::{PI, SQRT_2};
use std::collections::HashMap;
use ndarray_linalg::{Solve, Inverse};
use blas::sger;

// -----------------------------------------------------------------------------
// Custom error function approximation for f32
// -----------------------------------------------------------------------------
fn erf(x: f32) -> f32 {
    let a1: f32 = 0.254829592;
    let a2: f32 = -0.284496736;
    let a3: f32 = 1.421413741;
    let a4: f32 = -1.453152027;
    let a5: f32 = 1.061405429;
    let p: f32 = 0.3275911;

    let sign = if x < 0.0 { -1.0 } else { 1.0 };
    let x = x.abs();

    let t = 1.0 / (1.0 + p * x);
    let y = 1.0 - ((((a5 * t + a4) * t + a3) * t + a2) * t + a1) * t * (-x * x).exp();
    sign * y
}

// -----------------------------------------------------------------------------
// Simple normal pdf and cdf functions for f32 (using erf)
// -----------------------------------------------------------------------------
#[inline]
fn norm_pdf(z: f32) -> f32 {
    (-0.5 * z * z).exp() / (2.0 * PI).sqrt()
}

#[inline]
fn norm_cdf(z: f32) -> f32 {
    0.5 * (1.0 + erf(z / SQRT_2))
}

// -----------------------------------------------------------------------------
// Probit model implementation using f32
// -----------------------------------------------------------------------------
struct Probit<'a> {
    endog: ArrayView1<'a, f32>,
    exog: ArrayView2<'a, f32>,
}

impl<'a> Probit<'a> {
    fn new(endog: ArrayView1<'a, f32>, exog: ArrayView2<'a, f32>) -> Self {
        Probit { endog, exog }
    }

    #[inline]
    fn cdf(&self, x: f32) -> f32 {
        let c = 0.5 * (1.0 + erf(x / SQRT_2));
        c.max(1e-15_f32).min(1.0 - 1e-15_f32)
    }

    #[inline]
    fn pdf(&self, x: f32) -> f32 {
        (-0.5 * x * x).exp() / (2.0 * PI).sqrt()
    }

    fn xbeta(&self, params: &ArrayView1<f32>, out: &mut Array1<f32>) {
        *out = self.exog.dot(params);
    }

    fn loglike(&self, xbeta: &ArrayView1<f32>) -> f32 {
        self.endog
            .iter()
            .zip(xbeta.iter())
            .map(|(y, xb)| {
                let q = 2.0 * y - 1.0;
                let z = q * xb;
                self.cdf(z).ln()
            })
            .sum()
    }

    fn score(&self, xbeta: &ArrayView1<f32>, grad: &mut Array1<f32>) {
        grad.fill(0.0);
        for (i, (y, xb)) in self.endog.iter().zip(xbeta.iter()).enumerate() {
            let q = 2.0 * y - 1.0;
            let z = q * xb;
            let pdf = self.pdf(z);
            let cdf = self.cdf(z);
            let adjusted = q * (pdf / cdf);
            let row = self.exog.row(i);
            for (g, &x) in grad.iter_mut().zip(row.iter()) {
                *g += x * adjusted;
            }
        }
    }

    // Hessian computed using BLAS’s single‑precision rank‑1 update (sger)
    fn hessian(&self, xbeta: &ArrayView1<f32>, hess: &mut Array2<f32>) {
        // Compute intermediate quantities.
        let q = self.endog.mapv(|y| 2.0 * y - 1.0);
        let z = &q * xbeta;
        let ratio = z.mapv(|zi| {
            let pdf = self.pdf(zi);
            let cdf = self.cdf(zi);
            pdf / cdf
        });
        let weights = z
            .iter()
            .zip(ratio.iter())
            .map(|(&zi, &r)| (r * r + r * zi).max(0.0))
            .collect::<Array1<f32>>();

        let (n, k) = self.exog.dim();
        // Allocate a flat vector for the Hessian in column‑major order.
        let mut hess_flat = vec![0.0_f32; k * k];

        // For each observation, update the Hessian via BLAS’s sger.
        for i in 0..n {
            let w = weights[i];
            let sqrt_w = w.sqrt();
            // Compute the scaled row vector: v = sqrt(w) * x_i.
            let v: Vec<f32> = self.exog.row(i).iter().map(|&x| x * sqrt_w).collect();

            let m = k as i32;
            let n_i32 = k as i32;
            let alpha = 1.0_f32;
            let incx = 1;
            let incy = 1;
            let lda = k as i32;
            unsafe {
                sger(m, n_i32, alpha, &v, incx, &v, incy, &mut hess_flat, lda);
            }
        }

        // Multiply by -1 to match the formulation.
        for elem in &mut hess_flat {
            *elem = -*elem;
        }

        // Convert the flat, column‑major Hessian into an Array2.
        let hess_array = Array2::from_shape_vec((k, k), hess_flat)
            .expect("Hessian vector length must match matrix shape")
            .reversed_axes();
        *hess = hess_array;
    }

    fn fit_naive_newton(&self, max_iter: usize, tol: f32) -> (Array1<f32>, f32, bool, usize) {
        let k = self.exog.ncols();
        let mut params = Array1::zeros(k);
        let mut xbeta = Array1::zeros(self.exog.nrows());
        let mut grad = Array1::zeros(k);
        let mut hess = Array2::zeros((k, k));
        let mut ll_old: f32;
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

// -----------------------------------------------------------------------------
// Compute robust covariance given all inputs (using f32)
// -----------------------------------------------------------------------------
fn robust_covariance(
    exog: &ArrayView2<f32>,
    xbeta: &ArrayView1<f32>,
    endog: &ArrayView1<f32>,
    h_inv: &ArrayView2<f32>,
    cluster: Option<ArrayView2<f32>>,
) -> Array2<f32> {
    let nobs = exog.nrows();
    let kvars = exog.ncols();

    if cluster.is_none() {
        let mut M_flat = vec![0.0_f32; kvars * kvars];

        for i in 0..nobs {
            let q = 2.0 * endog[i] - 1.0;
            let z = q * xbeta[i];
            let pdf = (-0.5 * z * z).exp() / (2.0 * PI).sqrt();
            let cdf = (0.5 * (1.0 + erf(z / SQRT_2)))
                .max(1e-15_f32)
                .min(1.0 - 1e-15_f32);
            let ratio = q * pdf / cdf;

            let row_vec: Vec<f32> = exog.row(i).to_vec();

            let m = kvars as i32;
            let alpha = ratio;
            let incx = 1;
            let incy = 1;
            let lda = kvars as i32;
            unsafe {
                sger(m, m, alpha, &row_vec, incx, &row_vec, incy, &mut M_flat, lda);
            }
        }
        let M_array = Array2::from_shape_vec((kvars, kvars), M_flat)
            .expect("M vector length must match matrix shape")
            .reversed_axes();
        h_inv.view().dot(&M_array.view()).dot(&h_inv.view())
    } else {
        let mut M = Array2::<f32>::zeros((kvars, kvars));
        let cluster = cluster.unwrap();
        if cluster.ncols() != 1 {
            for i in 0..nobs {
                let q = 2.0 * endog[i] - 1.0;
                let z = q * xbeta[i];
                let pdf = (-0.5 * z * z).exp() / (2.0 * PI).sqrt();
                let cdf = (0.5 * (1.0 + erf(z / SQRT_2)))
                    .max(1e-15_f32)
                    .min(1.0 - 1e-15_f32);
                let ratio = q * pdf / cdf;

                let row = exog.row(i);
                for j in 0..kvars {
                    let xj = row[j] * ratio;
                    for k in 0..kvars {
                        M[(j, k)] += xj * row[k];
                    }
                }
            }
        } else {
            let mut cluster_map: HashMap<u32, Array1<f32>> = HashMap::new();
            // Note: f32::to_bits returns u32.
            for i in 0..nobs {
                let cl_val = cluster[[i, 0]];
                let key = cl_val.to_bits();
                let q = 2.0 * endog[i] - 1.0;
                let z = q * xbeta[i];
                let pdf = (-0.5 * z * z).exp() / (2.0 * PI).sqrt();
                let cdf = (0.5 * (1.0 + erf(z / SQRT_2)))
                    .max(1e-15_f32)
                    .min(1.0 - 1e-15_f32);
                let ratio = q * pdf / cdf;

                let row = exog.row(i);
                let entry = cluster_map.entry(key).or_insert_with(|| Array1::zeros(kvars));
                for (g, &x) in entry.iter_mut().zip(row.iter()) {
                    *g += x * ratio;
                }
            }
            for score in cluster_map.values() {
                M += &score.view().insert_axis(Axis(1)).dot(&score.view().insert_axis(Axis(0)));
            }
        }
        h_inv.view().dot(&M.view()).dot(&h_inv.view())
    }
}

// -----------------------------------------------------------------------------
// Helper function: model_fit returns the fitted model components using f32
// -----------------------------------------------------------------------------
fn model_fit<'a>(
    exog: &'a Array2<f32>,
    endog: ArrayView1<'a, f32>,
    max_iter: usize,
    tol: f32,
    robust: bool,
    cluster_vars: Option<&PyAny>,
) -> PyResult<(Array1<f32>, f32, bool, usize, Array2<f32>)> {
    let probit = Probit::new(endog, exog.view());
    let (params, llf, converged, iterations) = probit.fit_naive_newton(max_iter, tol);
    let mut xbeta = Array1::zeros(exog.nrows());
    probit.xbeta(&params.view(), &mut xbeta);
    let mut hess = Array2::zeros((params.len(), params.len()));
    probit.hessian(&xbeta.view(), &mut hess);
    let mut cov_final = match hess.inv() {
        Ok(inv_hess) => -inv_hess,
        Err(_) => {
            eprintln!("Hessian singular => using identity for covariance");
            -Array2::<f32>::eye(exog.ncols())
        }
    };

    if robust {
        let cluster_view = if let Some(obj) = cluster_vars {
            let arr_2d = obj.downcast::<PyArray2<f32>>()?;
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

        let h_inv = cov_final.mapv(|x| -x);
        cov_final = robust_covariance(&exog.view(), &xbeta.view(), &endog, &h_inv.view(), cluster_view);
    }

    Ok((params, llf, converged, iterations, cov_final))
}

// -----------------------------------------------------------------------------
// PyO3 classes for the Probit model and results (using f32)
// -----------------------------------------------------------------------------
#[pyclass]
#[derive(Clone)]
struct RustProbitModel {
    exog_: Py<PyArray2<f32>>,
    endog_: Py<PyArray1<f32>>,
    exog_names_: Vec<String>,
}

#[pymethods]
impl RustProbitModel {
    #[getter]
    fn exog(&self) -> Py<PyArray2<f32>> {
        self.exog_.clone()
    }
    #[getter]
    fn endog(&self) -> Py<PyArray1<f32>> {
        self.endog_.clone()
    }
    #[getter]
    fn exog_names(&self) -> Vec<String> {
        self.exog_names_.clone()
    }
}

#[pyclass]
struct RustProbitResults {
    params_: Py<PyArray1<f32>>,
    cov_: Py<PyArray2<f32>>,
    model_: RustProbitModel,
    loglike_: f32,
    iterations_: usize,
    converged_: bool,
}

#[pymethods]
impl RustProbitResults {
    #[getter]
    fn params(&self) -> Py<PyArray1<f32>> {
        self.params_.clone()
    }
    #[getter]
    fn cov_params(&self) -> Py<PyArray2<f32>> {
        self.cov_.clone()
    }
    #[getter]
    fn model(&self) -> RustProbitModel {
        self.model_.clone()
    }
    #[getter]
    fn loglike(&self) -> f32 {
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

// -----------------------------------------------------------------------------
// fit_probit: Fitting the probit model using f32 arrays
// -----------------------------------------------------------------------------
#[pyfunction]
#[allow(clippy::too_many_arguments)]
fn fit_probit(
    py: Python<'_>,
    endog_py: PyReadonlyArrayDyn<f32>,
    exog_py: PyReadonlyArray2<f32>,
    max_iter: Option<usize>,
    tol: Option<f32>,
    robust: Option<bool>,
    cluster_vars: Option<&PyAny>,
    intercept: Option<bool>,
) -> PyResult<RustProbitResults> {
    // Process the endogenous variable.
    let endog_view = endog_py.as_array();
    let endog: ndarray::ArrayView1<f32> = if endog_view.ndim() == 2 && endog_view.shape()[1] == 1 {
        endog_view.into_dimensionality::<ndarray::Ix1>().map_err(|_| {
            PyErr::new::<pyo3::exceptions::PyValueError, _>(
                "Failed to flatten endog array with shape (N,1)",
            )
        })?
    } else if endog_view.ndim() == 1 {
        endog_view.into_dimensionality::<ndarray::Ix1>().unwrap()
    } else {
        return Err(PyErr::new::<pyo3::exceptions::PyValueError, _>(
            "endog must be 1-dimensional or 2-dimensional with shape (N,1)",
        ));
    };

    let endog_owned_for_fit = endog.to_owned();

    // Process the exogenous variables.
    let exog = exog_py.as_array();
    let intercept = intercept.unwrap_or(true);
    let exog_with_intercept = if intercept {
        let nobs = exog.nrows();
        let ones = Array2::ones((nobs, 1));
        ndarray::concatenate(Axis(1), &[ones.view(), exog.view()]).map_err(|e| {
            PyErr::new::<pyo3::exceptions::PyValueError, _>(format!(
                "Failed to concatenate intercept: {}",
                e
            ))
        })?
    } else {
        exog.to_owned()
    };

    let exog_names = if intercept {
        let mut names = vec!["intercept".to_string()];
        names.extend((0..exog_with_intercept.ncols() - 1).map(|j| format!("x{}", j)));
        names
    } else {
        (0..exog_with_intercept.ncols()).map(|j| format!("x{}", j)).collect()
    };

    let (params, llf, converged, iterations, cov_final) = {
        model_fit(
            &exog_with_intercept,
            endog_owned_for_fit.view(),
            max_iter.unwrap_or(35),
            tol.unwrap_or(1e-6_f32),
            robust.unwrap_or(false),
            cluster_vars,
        )?
    };

    let params_py = PyArray1::from_owned_array(py, params).into();
    let cov_py = PyArray2::from_owned_array(py, cov_final).into();
    let exog_py_owned = PyArray2::from_owned_array(py, exog_with_intercept).into();
    let endog_py_owned = PyArray1::from_owned_array(py, endog_owned_for_fit).into();

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

// -----------------------------------------------------------------------------
// Helper functions for the AME function (using f32)
// -----------------------------------------------------------------------------
fn add_significance_stars(p: f32) -> &'static str {
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

fn as_array2_f32<'py>(obj: &'py PyAny) -> PyResult<ArrayView2<'py, f32>> {
    let pyarray = obj.downcast::<PyArray2<f32>>()?;
    Ok(unsafe { pyarray.as_array() })
}

fn as_array1_f32<'py>(obj: &'py PyAny) -> PyResult<ArrayView1<'py, f32>> {
    let pyarray = obj.downcast::<PyArray1<f32>>()?;
    Ok(unsafe { pyarray.as_array() })
}

fn extract_probit_model_components<'py>(
    _py: Python<'py>,
    probit_model: &'py PyAny,
) -> PyResult<(Array1<f32>, Array2<f32>, Vec<String>, Array2<f32>)> {
    let params_obj = probit_model.getattr("params")?;
    let beta_view = as_array1_f32(params_obj)?;
    let beta = beta_view.to_owned();

    let cov_obj = probit_model.getattr("cov_params")?;
    let cov_view = as_array2_f32(cov_obj)?;
    let cov_beta = cov_view.to_owned();

    let exog_names_py: Vec<String> = probit_model
        .getattr("model")?
        .getattr("exog_names")?
        .extract()?;

    let x_obj = probit_model.getattr("model")?.getattr("exog")?;
    let x_view = as_array2_f32(x_obj)?;
    let X = x_view.to_owned();

    Ok((beta, cov_beta, exog_names_py, X))
}

// -----------------------------------------------------------------------------
// AME (Average Marginal Effects) function using f32
// -----------------------------------------------------------------------------
#[pyfunction]
fn ame<'py>(
    py: Python<'py>,
    probit_model: &'py PyAny,  // The Python Probit model
    chunk_size: Option<usize>, // Optional chunk size for processing
) -> PyResult<&'py PyAny> {
    let params_obj = probit_model.getattr("params")?;
    let beta_view = params_obj.downcast::<PyArray1<f32>>()?;
    let beta = unsafe { beta_view.as_array() }.to_owned();

    let cov_obj = probit_model.call_method0("cov_params")?;
    let cov_view = cov_obj.downcast::<PyArray2<f32>>()?;
    let cov_beta = unsafe { cov_view.as_array() }.to_owned();

    let mut exog_names: Vec<String> = probit_model
        .getattr("model")?
        .getattr("exog_names")?
        .extract()?;
    
    let x_obj = probit_model.getattr("model")?.getattr("exog")?;
    let X = unsafe { x_obj.downcast::<PyArray2<f32>>()?.as_array() };

    let (n, k) = (X.nrows(), X.ncols());
    let chunk = chunk_size.unwrap_or(n);

    // STEP 2: Identify intercept columns.
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
        if X.column(j).iter().all(|&v| (v - X[(0, j)]).abs() < 1e-8_f32) {
            if !intercept_indices.contains(&j) {
                intercept_indices.push(j);
                exog_names[j] = "Intercept".to_string();
            }
        }
    }

    // STEP 3: Identify discrete variables (excluding intercepts).
    let is_discrete: Vec<usize> = (0..k)
        .filter(|&j| {
            if intercept_indices.contains(&j) {
                false
            } else {
                X.column(j).iter().all(|&v| v == 0.0 || v == 1.0)
            }
        })
        .collect();

    // STEP 4: Process data in chunks to compute average marginal effects (AME).
    let mut sum_ame = vec![0.0_f32; k];
    let mut partial_jl_sums = vec![0.0_f32; k * k];

    let mut idx_start = 0;
    while idx_start < n {
        let idx_end = (idx_start + chunk).min(n);
        let x_chunk = X.slice(ndarray::s![idx_start..idx_end, ..]);
        let z_chunk = x_chunk.dot(&beta);
        let phi_vals = z_chunk.mapv(|z| norm_pdf(z));

        // Process discrete features.
        for &j in &is_discrete {
            if intercept_indices.contains(&j) {
                continue;
            }
            let xj_col = x_chunk.column(j);
            let beta_j = beta[j];
            let delta_j1 = xj_col.mapv(|x| if x == 0.0 { beta_j } else { 0.0 });
            let delta_j0 = xj_col.mapv(|x| if x == 1.0 { -beta_j } else { 0.0 });
            let z_j1 = &z_chunk + &delta_j1;
            let z_j0 = &z_chunk + &delta_j0;
            let cdf_diff_sum = z_j1.mapv(|z| norm_cdf(z)).sum()
                - z_j0.mapv(|z| norm_cdf(z)).sum();
            sum_ame[j] += cdf_diff_sum;

            let pdf_j1 = z_j1.mapv(|z| norm_pdf(z));
            let pdf_j0 = z_j0.mapv(|z| norm_pdf(z));
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
                    -beta_j * (z_chunk.clone() * &x_chunk.column(l)).dot(&phi_vals)
                };
                partial_jl_sums[j * k + l] += grad;
            }
        }
        idx_start = idx_end;
    }

    // STEP 5: Final calculations.
    let ame: Vec<f32> = sum_ame.iter().map(|v| v / n as f32).collect();
    let mut grad_ame = Array2::zeros((k, k));
    for j in 0..k {
        for l in 0..k {
            grad_ame[(j, l)] = partial_jl_sums[j * k + l] / n as f32;
        }
    }
    let cov_ame = grad_ame.dot(&cov_beta).dot(&grad_ame.t());
    let var_ame: Vec<f32> = cov_ame.diag().iter().map(|&v| v.max(0.0)).collect();
    let se_ame: Vec<f32> = var_ame.iter().map(|v| v.sqrt()).collect();

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
            f32::NAN
        };
        z_vals.push(z);
        let p = 2.0 * (1.0 - norm_cdf(z.abs()));
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

// -----------------------------------------------------------------------------
// PyO3 Module Definition
// -----------------------------------------------------------------------------
#[pymodule]
fn febolt(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(fit_probit, m)?)?;
    m.add_function(wrap_pyfunction!(ame, m)?)?;
    Ok(())
}
