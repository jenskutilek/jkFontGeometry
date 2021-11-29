use pyo3::prelude::*;


#[pyfunction]
fn half_point(_py: Python, point0: Vec<f32>, point1: Vec<f32>) -> PyResult<Vec<f32>> {
    let half: Vec<f32> = (0..2).map(|i| (point0[i] + point1[i]) * 0.5).collect();

    Ok(half)
}

#[pymodule]
fn fastgeometry(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(half_point, m)?)?;

    Ok(())
}
