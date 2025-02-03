use pyo3::prelude::*;
use itertools::Itertools;

mod tests; // Import the tests module

/// Calculate the probability that none of the specified events occur in any of the n trials.
fn single_event_prob(n: usize, event_indices: &[usize], probabilities: &[Vec<f64>]) -> f64 {
    (0..n).fold(1.0, |acc, i| {
        acc * (1.0 - event_indices.iter().map(|&j| probabilities[i][j]).sum::<f64>())
    })
}

/// Calculate the filling probability of observing each of the m events at least once
/// among the n independent discrete random variables with given probabilities.
#[pyfunction]
fn filling_prob(n: usize, m: usize, probabilities: Vec<Vec<f64>>) -> PyResult<f64> {
    if probabilities.len() != n {
        return Err(pyo3::exceptions::PyValueError::new_err("Length of probabilities should be equal to n"));
    }

    for p in &probabilities {
        if p.len() != m {
            return Err(pyo3::exceptions::PyValueError::new_err("Each probability list should have a length of m"));
        }
    }

    let mut filling_prob = 1.0;
    
    for k in 1..=m {
        let mut sum_comb = 0.0;
        
        for event_indices in (0..m).combinations(k) {
            sum_comb += single_event_prob(n, &event_indices, &probabilities);
        }
        
        filling_prob -= (-1.0f64).powi((k + 1) as i32) * sum_comb;
    }
    
    Ok(filling_prob)
}

/// A module to be used in Python.
#[pymodule]
fn procol(module: &Bound<'_, PyModule>) -> PyResult<()> {
    module.add_function(wrap_pyfunction!(filling_prob, module)?)?;
    Ok(())
}
