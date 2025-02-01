use crate::solution::{Solute, Solution};
use crate::water::water;

pub fn NaCl()->Solute{
    Solute{
        molar_mass: 58.44,
        number_ions: 2,
        density: 2170.0,
        refractive_index: 1.5442,
    }
}

fn aqueous_NaCl_diffusion(mfs:f64, temperature:f64)->f64{
    let D_0=1e-9*(1.955 - 20.42*mfs + 141.7*mfs.powi(2) - 539.8*mfs.powi(3) + 995.6*mfs.powi(4) - 698.7*mfs.powi(5));
    let water_viscosity =  |T:f64| -1.748e-5*(T-273.0)+1.336e-3;
    D_0*temperature/293.0*water_viscosity(293.0)/water_viscosity(temperature)
}
    

pub fn aqueous_NaCl() ->Solution{
    Solution{
        solvent: water(),
        solute: NaCl(),
        diffusion: Box::new(aqueous_NaCl_diffusion),
        solubility_limit: 0.3,
        activity_coefficients: vec![48.5226539, -158.04388699, 186.59427048, -93.88696437, 19.28939256, -2.99894206, -0.47652352, 1.],
        density_coefficients: vec![-940.62808, 2895.88613, -2131.05669, 1326.69542, -55.33776, 998.2],
        mfs_coefficients: vec![-2.83205492e-14,  1.78786638e-10, -4.82844409e-07,  9.63181430e-04,1.68570161e-03],
    }
}