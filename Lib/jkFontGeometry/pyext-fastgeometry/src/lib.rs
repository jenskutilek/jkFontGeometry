use pyo3::prelude::*;


// internal functions

fn line_coefficients(point0: Vec<f32>, point1: Vec<f32>) -> Vec<f32> {
    // Calculate coefficients a, b, c for a 2D line from point0 to point1
    let mut coefficients: Vec<f32> = Vec::with_capacity(3);
    // a
    coefficients.push(point0[1] - point1[1]);
    // b
    coefficients.push(point1[0] - point0[0]);
    // c
    coefficients.push(- point0[0] * point1[1] + point1[0] * point1[0]);

    return coefficients
}

fn intersect_coeffs(line1: Vec<f32>, line2: Vec<f32>) -> Vec<f32> {
    // Intersect two 2D lines line0, line1 using their coefficients.

    let mut intersection: Vec<f32> = Vec::with_capacity(2);
    let d: f32 = line1[0] * line2[1] - line1[1] * line2[0];

    if d != 0.0 {
        let dx: f32 = line1[2] * line2[1] - line1[1] * line2[2];
        let dy: f32 = line1[0] * line2[2] - line1[2] * line2[0];
        intersection.push(dx / d);
        intersection.push(dy / d);
    }

    return intersection
}



// functions exposed to Python

#[pyfunction]
fn half_point(_py: Python, point0: Vec<f32>, point1: Vec<f32>) -> PyResult<Vec<f32>> {
    let half: Vec<f32> = (0..2).map(|i| (point0[i] + point1[i]) * 0.5).collect();

    Ok(half)
}

#[pyfunction]
fn get_cubic_point(_py: Python, t: f32, p0: Vec<f32>, p1: Vec<f32>, p2: Vec<f32>, p3: Vec<f32>) -> PyResult<Vec<f32>> {
    let mut p: Vec<f32> = Vec::with_capacity(2);
    if t == 0.0 {
        p = p0
    } else if t == 1.0 {
        p = p3
    } else {
        let cx = (p1[0] - p0[0]) * 3.0;
        let cy = (p1[1] - p0[1]) * 3.0;

        let bx = (p2[0] - p1[0]) * 3.0 - cx;
        let by = (p2[1] - p1[1]) * 3.0 - cy;

        let ax = p3[0] - p0[0] - cx - bx;
        let ay = p3[1] - p0[1] - cy - by;

        let t3 = t * t * t;
        let t2 = t * t;

        p.push(ax * t3 + bx * t2 + cx * t + p0[0]);
        p.push(ay * t3 + by * t2 + cy * t + p0[1]);
    }

    Ok(p)
}

#[pyfunction]
fn get_quadratic_point(_py: Python, t: f32, p0: Vec<f32>, p1: Vec<f32>, p2: Vec<f32>) -> PyResult<Vec<f32>> {
    let mut p: Vec<f32> = Vec::with_capacity(2);
    if t == 0.0 {
        p = p0
    } else if t == 1.0 {
        p = p2
    } else {
        let a = (1.0 - t) * (1.0 - t);
        let b = 2.0 * t * (1.0 - t);
        let c = t * t;

        p.push(a * p0[0] + b * p1[0] + c * p2[0]);
        p.push(a * p0[1] + b * p1[1] + c * p2[1]);
    }

    Ok(p)
}

#[pyfunction]
fn intersect(_py: Python, p0: Vec<f32>, p1: Vec<f32>, p2: Vec<f32>, p3: Vec<f32>) -> PyResult<Vec<f32>> {
    // Intersect two 2D lines, with the first line defined by p0 to p1,
    // and the second line from p2 to p3.

    let line1: Vec<f32> = line_coefficients(p0, p1);
    let line2: Vec<f32> = line_coefficients(p2, p3);

    let intersection: Vec<f32> = intersect_coeffs(line1, line2);

    Ok(intersection)
}


// The Python module

#[pymodule]
fn fastgeometry(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(get_cubic_point, m)?)?;
    m.add_function(wrap_pyfunction!(get_quadratic_point, m)?)?;
    m.add_function(wrap_pyfunction!(half_point, m)?)?;
    m.add_function(wrap_pyfunction!(intersect, m)?)?;

    Ok(())
}
