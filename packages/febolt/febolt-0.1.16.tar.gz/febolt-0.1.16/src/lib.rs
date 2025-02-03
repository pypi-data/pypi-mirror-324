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
use ndarray_linalg::Solve;

// -----------------------------------------------------------------------------
// Helper: Solve a matrix system A * X = B for X, where B is a 2-D array.
// This function solves for each column of B separately.
fn solve_matrix(
    a: &Array2<f64>,
    b: &Array2<f64>,
) -> Result<Array2<f64>, ndarray_linalg::error::LinalgError> {
    let (n, m) = b.dim();
    let mut sol = Array2::<f64>::zeros((n, m));
    for j in 0..m {
        let bcol = b.column(j).to_owned();
        let xcol = a.solve(&bcol)?;
        sol.column_mut(j).assign(&xcol);
    }
    Ok(sol)
}

// -----------------------------------------------------------------------------
// Minimal BFGS approach without repeated Hessian -- vectorized update using outer()
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

    // initialize B as identity
    let mut B = Array2::<f64>::eye(k);
    let mut converged = false;
    let mut iter_used = 0;

    for iter in 0..max_iter {
        iter_used = iter;

        // direction = -B * g
        let p = -B.dot(&g_old);

        // step-halving line search
        let mut step_size = 1.0;
        let old_ll = ll_old;
        let mut x_new = &x + &(step_size * &p);
        let mut ll_new = ll_fn(&x_new);

        let mut halving_count = 0;
        while ll_new < old_ll && halving_count < 10 {
            step_size *= 0.5;
            x_new = &x + &(step_size * &p);
            ll_new = ll_fn(&x_new);
            halving_count += 1;
        }

        let g_new = grad_fn(&x_new);
        let diff_ll = (ll_new - ll_old).abs();

        // BFGS update:
        //   s = x_new - x, y = g_new - g_old,
        //   B = B + (s sᵀ)/(sᵀ y) - (B y yᵀ B)/(yᵀ B y)
        let s = &x_new - &x;
        let y = &g_new - &g_old;
        let ys = y.dot(&s);
        if ys.abs() > 1e-14 {
            let s_col = s.clone().insert_axis(Axis(1));
            let term1 = s_col.dot(&s_col.t()) / ys;
            let By = B.dot(&y);
            let denom2 = y.dot(&By);
            if denom2.abs() > 1e-14 {
                let By_col = By.clone().insert_axis(Axis(1));
                let term2 = By_col.dot(&By_col.t()) / denom2;
                B = B + &term1 - &term2;
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
// Minimal Probit Model with vectorized likelihood, gradient and Hessian
struct Probit {
    endog: Array1<f64>,
    exog: Array2<f64>,
    dist: Normal, // using statrs for the normal distribution
}

impl Probit {
    fn new(endog: Array1<f64>, exog: Array2<f64>) -> Self {
        Probit {
            endog,
            exog,
            dist: Normal::new(0.0, 1.0).unwrap(),
        }
    }

    // cdf clamped to avoid log(0)
    fn cdf(&self, z: f64) -> f64 {
        let c = self.dist.cdf(z);
        c.max(1e-15).min(1.0 - 1e-15)
    }

    fn pdf(&self, z: f64) -> f64 {
        self.dist.pdf(z)
    }

    // Use dot product on the i-th row.
    fn xbeta(&self, params: &Array1<f64>, i: usize) -> f64 {
        self.exog.row(i).dot(params)
    }

    // Compute log-likelihood in a vectorized way.
    fn loglike(&self, params: &Array1<f64>) -> f64 {
        let xbeta = self.exog.dot(params);
        let q = self.endog.mapv(|y| 2.0 * y - 1.0);
        let z = &q * &xbeta;
        z.iter().map(|&z_i| self.cdf(z_i).ln()).sum()
    }

    // Compute gradient as exogᵀ * ratio.
    fn grad(&self, params: &Array1<f64>) -> Array1<f64> {
        let xbeta = self.exog.dot(params);
        let q = self.endog.mapv(|y| 2.0 * y - 1.0);
        let z = &q * &xbeta;
        let ratio = Array1::from_iter(
            z.iter()
                .zip(q.iter())
                .map(|(&z_i, &q_i)| (q_i * self.pdf(z_i)) / self.cdf(z_i)),
        );
        self.exog.t().dot(&ratio)
    }

    // Compute Hessian as -Xᵀ D X with D a diagonal weight matrix.
    fn hessian(&self, params: &Array1<f64>) -> Array2<f64> {
        let xbeta = self.exog.dot(params);
        let q = self.endog.mapv(|y| 2.0 * y - 1.0);
        let z = &q * &xbeta;
        let lam = Array1::from_iter(
            z.iter()
                .zip(q.iter())
                .map(|(&z_i, &q_i)| (q_i * self.pdf(z_i)) / self.cdf(z_i)),
        );
        let weight = &lam * (&lam + &xbeta);
        // Multiply each row of exog by its weight.
        let weighted_exog = &self.exog * &weight.insert_axis(Axis(1));
        -self.exog.t().dot(&weighted_exog)
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
// White cross-product computed via a simple matrix multiplication
fn calc_white_crossprod(s_obs: &Array2<f64>) -> Array2<f64> {
    s_obs.t().dot(s_obs)
}

// -----------------------------------------------------------------------------
// Combine cluster keys (string manipulation)
// -----------------------------------------------------------------------------
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
// fit_probit function => BFGS estimation, final Cov, robust/cluster covariance
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
    // Flatten endog to Array1<f64>
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
                    format!("endog must be shape (nobs,) or (nobs,1). got=({},{:?})", r, c)
                ));
            }
        }
    };

    let exog = unsafe { exog_py.as_array() }.to_owned();
    let max_iter = max_iter.unwrap_or(35);
    let tol = tol.unwrap_or(1e-6);
    let do_robust = robust.unwrap_or(false);

    // BFGS estimation
    let model_data = Probit::new(endog.clone(), exog.clone());
    let (params, llf, converged, iterations) = model_data.fit_bfgs(max_iter, tol);

    // Compute Hessian.
    let hess_final = model_data.hessian(&params);
    let kvars = exog.ncols();
    let identity = Array2::<f64>::eye(kvars);

    // Compute classical covariance: Cov = -H⁻¹, by solving H * X = I.
    let cov_classical = match solve_matrix(&hess_final, &identity) {
        Ok(x) => -x,
        Err(_) => {
            eprintln!("Hessian singular => using identity for covariance");
            Array2::<f64>::eye(kvars)
        }
    };

    // Robust/cluster covariance adjustment.
    // Instead of allocating a huge s_obs_mat of shape (nobs,kvars),
    // we accumulate the cross-product directly.
    let cov_final = if do_robust {
        let nobs = endog.len();
        let mut M = Array2::<f64>::zeros((kvars, kvars));
        for i in 0..nobs {
            let q = 2.0 * endog[i] - 1.0;
            let z = q * model_data.xbeta(&params, i);
            let ratio = (q * model_data.pdf(z)) / model_data.cdf(z);
            let row = exog.row(i);
            for r in 0..kvars {
                for c in 0..kvars {
                    M[[r, c]] += ratio * ratio * row[r] * row[c];
                }
            }
        }
        let final_mat = if let Some(obj) = cluster_vars {
            if obj.is_none() {
                M
            } else {
                // For clustered covariance, accumulate per-cluster.
                let arr_2d = obj.downcast::<PyArray2<f64>>()?;
                let cluster_view = unsafe { arr_2d.as_array() }.to_owned();
                if cluster_view.nrows() != nobs {
                    return Err(pyo3::exceptions::PyValueError::new_err(
                        format!("cluster mismatch: got {} rows, expected {}", cluster_view.nrows(), nobs)
                    ));
                }
                let keys = combine_cluster_keys(&cluster_view);
                let mut group_sums: HashMap<String, Array1<f64>> = HashMap::new();
                for (i, key) in keys.iter().enumerate() {
                    let entry = group_sums.entry(key.clone()).or_insert_with(|| Array1::<f64>::zeros(kvars));
                    let q = 2.0 * endog[i] - 1.0;
                    let z = q * model_data.xbeta(&params, i);
                    let ratio = (q * model_data.pdf(z)) / model_data.cdf(z);
                    let row = exog.row(i);
                    for j in 0..kvars {
                        entry[j] += ratio * row[j];
                    }
                }
                let mut M_cluster = Array2::<f64>::zeros((kvars, kvars));
                for (_key, sumv) in group_sums {
                    let sumv_col = sumv.insert_axis(Axis(1));
                    M_cluster = M_cluster + &sumv_col.dot(&sumv_col.t());
                }
                M_cluster
            }
        } else {
            M
        };

        // Robust covariance: compute robust covariance = -H⁻¹ * final_mat * H⁻¹.
        let h_inv_times_final = match solve_matrix(&hess_final, &final_mat) {
            Ok(x) => x,
            Err(_) => {
                eprintln!("Hessian singular during robust solve => using identity for covariance");
                Array2::<f64>::eye(kvars)
            }
        };

        let robust_cov_intermediate = match solve_matrix(&hess_final, &h_inv_times_final) {
            Ok(y) => y,
            Err(_) => {
                eprintln!("Hessian singular during robust solve => using identity for covariance");
                Array2::<f64>::eye(kvars)
            }
        };

        -robust_cov_intermediate
    } else {
        cov_classical
    };

    let params_py = params.into_pyarray(py).to_owned();
    let cov_py = cov_final.into_pyarray(py).to_owned();
    let exog_py_ = exog.into_pyarray(py).to_owned();
    let endog_py_ = endog.into_pyarray(py).to_owned();

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
