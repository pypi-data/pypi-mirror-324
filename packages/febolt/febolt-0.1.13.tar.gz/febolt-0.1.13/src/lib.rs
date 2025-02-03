// src/lib.rs
extern crate libm;
extern crate statrs;

use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use pyo3::types::{PyAny, PyDict};
use pyo3::exceptions::PyValueError;
use numpy::{IntoPyArray, PyArray1, PyArray2, PyReadonlyArray1, PyReadonlyArray2, PyReadonlyArrayDyn};
use ndarray::{Array1, Array2, Axis, ArrayView1, ArrayView2};
use statrs::distribution::{Continuous, ContinuousCDF, Normal};
use std::f64::consts::{PI, SQRT_2};
use std::collections::HashMap;
use std::hash::{Hash, Hasher};
use std::fmt::Write as _;
use statrs::function::erf::erf;

// Bring in ndarray-linalg traits for solving linear systems and inversion.
use ndarray_linalg::{Solve, Inverse};
use ndarray::linalg::{general_mat_vec_mul, general_mat_mul};

/// Replace these with calls to your actual BLAS wrapper.
/// In production you might replace these with calls to a proper BLAS library.
mod BLAS {
    use ndarray::{Array1, Array2, ArrayView1, ArrayView2};
    use ndarray::linalg::{general_mat_vec_mul, general_mat_mul};

    /// Optimized matrix–vector multiplication: y := alpha * A*x + beta*y.
    pub fn gemv(alpha: f64, a: &ArrayView2<f64>, x: &ArrayView1<f64>, beta: f64, y: &mut Array1<f64>) {
        general_mat_vec_mul(alpha, a, x, beta, y);
    }

    /// Optimized matrix–matrix multiplication: C := alpha * A*B + beta * C.
    pub fn gemm(alpha: f64, a: &Array2<f64>, b: &ArrayView2<f64>, beta: f64, c: &mut Array2<f64>) {
        general_mat_mul(alpha, a, b, beta, c);
    }

    /// A simple (non-optimized) implementation of a symmetric rank‑k update:
    /// C := alpha * A * A^T + beta * C.
    pub fn syrk(alpha: f64, a: &ArrayView2<f64>, beta: f64, c: &mut Array2<f64>) {
        let prod = a.dot(&a.t());
        *c = prod.mapv(|v| alpha * v) + c.mapv(|v| beta * v);
    }

    /// Rank‑2 update: A := alpha * (x*y^T + y*x^T) + A.
    pub fn syr2(alpha: f64, x: &ArrayView1<f64>, y: &ArrayView1<f64>, a: &mut Array2<f64>) {
        let n = x.len();
        for i in 0..n {
            for j in 0..n {
                a[[i, j]] += alpha * (x[i] * y[j] + y[i] * x[j]);
            }
        }
    }

    /// Rank‑1 update: A := alpha * x*x^T + A.
    pub fn syr(alpha: f64, x: &ArrayView1<f64>, a: &mut Array2<f64>) {
        let n = x.len();
        for i in 0..n {
            for j in 0..n {
                a[[i, j]] += alpha * x[i] * x[j];
            }
        }
    }

    /// Dot product.
    pub fn dot(x: &ArrayView1<f64>, y: &ArrayView1<f64>) -> f64 {
        x.dot(y)
    }
}

/// The Probit model holds views to the endogenous and exogenous data.
struct Probit<'a> {
    endog: ArrayView1<'a, f64>,
    exog: ArrayView2<'a, f64>, // note lifetime on exog
}

impl<'a> Probit<'a> {
    fn new(endog: ArrayView1<'a, f64>, exog: ArrayView2<'a, f64>) -> Self {
        Probit { endog, exog }
    }

    #[inline]
    fn cdf(&self, x: f64) -> f64 {
        let c: f64 = 0.5 * (1.0 + erf(x / SQRT_2));
        c.max(1e-15).min(1.0 - 1e-15)
    }

    #[inline]
    fn pdf(&self, x: f64) -> f64 {
        (-0.5 * x.powi(2)).exp() / (2.0 * PI).sqrt()
    }

    // BLAS-accelerated Xβ
    fn xbeta(&self, params: &ArrayView1<f64>, out: &mut Array1<f64>) {
        BLAS::gemv(1.0, &self.exog.view(), params, 0.0, out);
    }

    // Vectorized log-likelihood
    fn loglike(&self, xbeta: &ArrayView1<f64>) -> f64 {
        let q = self.endog.mapv(|y| 2.0 * y - 1.0);
        let z = &q * xbeta;
        z.mapv(|zi| self.cdf(zi).ln()).sum()
    }

    // BLAS-accelerated gradient
    // Inside your grad() method:
    fn grad(&self, xbeta: &ArrayView1<f64>, grad: &mut Array1<f64>) {
        let q = self.endog.mapv(|y| 2.0 * y - 1.0);
        let z = &q * xbeta;
        // First compute temp = pdf(z)/cdf(z) elementwise.
        let temp = z.mapv(|zi| self.pdf(zi) / self.cdf(zi));
        // Then compute the elementwise product of q and temp.
        let ratio = &q * &temp;
        grad.fill(0.0);
        // Use reversed_axes() instead of t() to get a "clean" transposed view.
        let a_t: Array2<f64> = self.exog.reversed_axes().to_owned();
        let a_t_view = a_t.view();
        BLAS::gemv(1.0, &a_t_view, &ratio.view(), 0.0, grad);
    }
    
    // Inside your hessian() method:
    fn hessian(&self, xbeta: &ArrayView1<f64>, hess: &mut Array2<f64>) {
        let q = self.endog.mapv(|y| 2.0 * y - 1.0);
        let z = &q * xbeta;
        // As in grad(), compute lam elementwise using the correct mapping.
        let lam = &q * &z.mapv(|zi| self.pdf(zi) / self.cdf(zi));
        let xbeta_owned = xbeta.to_owned();
        let sum = &lam + &xbeta_owned;
        let val = lam.mapv(|l| -l) * &sum;
        
        // val is already 1D; iterate over its scalar elements.
        let mut weighted_exog = self.exog.to_owned();
        for (i, &v) in val.iter().enumerate() {
            let sqrt_v = v.sqrt();  // v is an f64
            weighted_exog.row_mut(i).mapv_inplace(|x| x * sqrt_v);
        }
        BLAS::syrk(1.0, &weighted_exog.view(), 0.0, hess);
    }

    // Fit the model using a BFGS optimization routine.
    fn fit_bfgs(&self, max_iter: usize, tol: f64) -> (Array1<f64>, f64, bool, usize) {
        let k = self.exog.ncols();
        let n = self.exog.nrows();
        let mut x = Array1::zeros(k);
        let mut xbeta = Array1::zeros(n);
        let mut grad = Array1::zeros(k);
        let mut B = Array2::eye(k);
        self.xbeta(&x.view(), &mut xbeta);
        let mut ll_old = self.loglike(&xbeta.view());
        let mut converged = false;
        let mut iter_used = 0;

        for iter in 0..max_iter {
            iter_used = iter;
            self.grad(&xbeta.view(), &mut grad);
            let mut p = Array1::zeros(k);
            BLAS::gemv(-1.0, &B.view(), &grad.view(), 0.0, &mut p);
            let (x_new, ll_new) = self.backtracking_line_search(&x, &p, ll_old);

            // Check convergence.
            if (ll_new - ll_old).abs() < tol {
                x = x_new;
                ll_old = ll_new;
                converged = true;
                break;
            }

            self.xbeta(&x_new.view(), &mut xbeta);
            let mut grad_new = Array1::zeros(k);
            self.grad(&xbeta.view(), &mut grad_new);
            let s = &x_new - &x;
            let y = &grad_new - &grad;
            self.bfgs_update(&mut B, &s.view(), &y.view());
            x = x_new;
            ll_old = ll_new;
        }
        (x, ll_old, converged, iter_used)
    }

    // BFGS update for the inverse Hessian approximation.
    fn bfgs_update(&self, B: &mut Array2<f64>, s: &ArrayView1<f64>, y: &ArrayView1<f64>) {
        let ys_dot = BLAS::dot(y, s);
        if ys_dot.abs() > 1e-14 {
            let rho = 1.0 / ys_dot;
            let mut B_y = Array1::zeros(B.ncols());
            BLAS::gemv(1.0, &B.view(), y, 0.0, &mut B_y);
            BLAS::syr2(-rho, s, &B_y.view(), B);
            BLAS::syr(rho, s, B);
        }
    }

    // Backtracking line search to find a new iterate with improved log-likelihood.
    fn backtracking_line_search(&self, x: &Array1<f64>, p: &Array1<f64>, old_ll: f64) -> (Array1<f64>, f64) {
        let mut step = 1.0;
        let mut x_new = x + p * step;
        let mut xbeta_new = Array1::zeros(self.exog.nrows());
        for _ in 0..10 {
            self.xbeta(&x_new.view(), &mut xbeta_new);
            let ll_new = self.loglike(&xbeta_new.view());
            if ll_new > old_ll {
                return (x_new, ll_new);
            }
            step *= 0.5;
            x_new = x + p * step;
        }
        (x.clone(), old_ll)
    }
}

/// Compute the robust covariance matrix using BLAS-accelerated operations.
fn robust_covariance(
    exog: &ArrayView2<f64>,
    xbeta: &ArrayView1<f64>,
    endog: &ArrayView1<f64>,
    h_inv: &ArrayView2<f64>,
    cluster: Option<&ArrayView2<f64>>,
) -> Array2<f64> {
    let mut scores = exog.to_owned();
    scores.axis_iter_mut(Axis(0))
        .zip(endog.iter())
        .zip(xbeta.iter())
        .for_each(|((mut row, &y), &xb)| {
            let q = 2.0 * y - 1.0;
            let z = q * xb;
            let ratio = q * (-0.5 * z.powi(2)).exp() / ((2.0 * PI).sqrt().max(1e-15));
            row *= ratio;
        });

    let M = match cluster {
        Some(cluster_view) => {
            let mut grouped: HashMap<String, Array1<f64>> = HashMap::new();
            for (i, score) in scores.axis_iter(Axis(0)).enumerate() {
                let key = cluster_view.row(i)
                    .iter()
                    .map(|v| format!("{:.4}", v))
                    .collect::<Vec<_>>()
                    .join("|");
                grouped.entry(key)
                    .and_modify(|s: &mut Array1<f64>| *s += &score)
                    .or_insert(score.to_owned());
            }
            let mut M = Array2::zeros((scores.ncols(), scores.ncols()));
            for sum in grouped.values() {
                let sum_col = sum.view().into_shape((sum.len(), 1)).unwrap();
                BLAS::syrk(1.0, &sum_col, 1.0, &mut M);
            }
            M
        }
        None => {
            let mut M = Array2::zeros((scores.ncols(), scores.ncols()));
            BLAS::syrk(1.0, &scores.t(), 0.0, &mut M);
            M
        }
    };

    let mut temp = Array2::zeros(M.dim());
    BLAS::gemm(1.0, &h_inv.to_owned(), &M.view(), 0.0, &mut temp);
    let mut cov = Array2::zeros(M.dim());
    BLAS::gemm(1.0, &temp, &h_inv.view(), 0.0, &mut cov);
    cov
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

/// Fit the Probit model from Python.
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
    let endog_view = endog_py.as_array();
    let endog: ArrayView1<f64> = if endog_view.ndim() == 2 && endog_view.shape()[1] == 1 {
        endog_view.into_dimensionality::<ndarray::Ix1>().map_err(|_| {
            PyValueError::new_err("Failed to flatten endog array with shape (N,1)")
        })?
    } else if endog_view.ndim() == 1 {
        endog_view.into_dimensionality::<ndarray::Ix1>().unwrap()
    } else {
        return Err(PyValueError::new_err(
            "endog must be 1-dimensional or 2-dimensional with shape (N,1)",
        ));
    };

    let exog = exog_py.as_array();
    let probit = Probit::new(endog, exog);
    let max_iter = max_iter.unwrap_or(35);
    let tol = tol.unwrap_or(1e-6);
    let do_robust = robust.unwrap_or(false);

    let (params, llf, converged, iterations) = probit.fit_bfgs(max_iter, tol);
    let mut xbeta = Array1::zeros(exog.nrows());
    probit.xbeta(&params.view(), &mut xbeta);

    let mut hess = Array2::zeros((params.len(), params.len()));
    probit.hessian(&xbeta.view(), &mut hess);
    let cov_final = match hess.inv() {
        Ok(inv_hess) => -inv_hess,
        Err(_) => {
            eprintln!("Hessian singular => using identity for covariance");
            -Array2::<f64>::eye(exog.ncols())
        }
    };

    let cov_final = if do_robust {
        let cluster_view = if let Some(obj) = cluster_vars {
            let arr_2d = obj.downcast::<PyArray2<f64>>()?;
            let view = unsafe { arr_2d.as_array() };
            if view.nrows() != exog.nrows() {
                return Err(PyValueError::new_err(format!(
                    "Cluster vars has {} rows, expected {}",
                    view.nrows(),
                    exog.nrows()
                )));
            }
            Some(view)
        } else {
            None
        };
        let h_inv = cov_final.mapv(|x| -x);
        robust_covariance(&exog.view(), &xbeta.view(), &endog, &h_inv.view(), cluster_view.as_ref())
    } else {
        cov_final
    };

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
