pub fn polynomial(coefficients: &[f64], x: f64) -> f64 {
    let n = coefficients.len();
    coefficients
        .iter()
        .enumerate()
        .fold(0.0, |acc, (i, &coefficient)| {
            coefficient * x.powi((n - i - 1) as i32)
        })
}
