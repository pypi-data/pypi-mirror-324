mod droplet;
mod solution;
mod fit;
mod constants;
mod environment;
mod mesh;
mod water;
mod solution_definitions;

use pyo3::prelude::*;
use crate::droplet::Droplet;
use crate::environment::{atmosphere};
use crate::mesh::Mesh;
use crate::solution::{Solution, Suspension};

#[pyfunction]
pub fn y_prime(state:Vec<f64>, solution_string: String, environment:(f64,f64,f64), suspension_string: String, suspension_radius:f64)->Vec<f64>{
    let solution = Solution::get(solution_string);
    let suspension = Suspension::get(suspension_string,suspension_radius);
    let environment = atmosphere(environment.0,environment.1,environment.2);
    let solvent_mass = state[0];
    let temperatures = &state[1..100+1];
    let log_solute_mass = &state[100+1..2*100+1];
    let log_particle_mass = &state[2*100+1..3*100+1];
    let positions = &state[3*100+1..4*100+1];
    let velocities = &state[4*100+1..5*100+1];
    let mesh = Mesh::new_from_data(positions,velocities,100);
    let droplet = Droplet::new_from_state(solution, environment, suspension, mesh, solvent_mass,
                                          Vec::from(temperatures), Vec::from(log_solute_mass), Vec::from(log_particle_mass));
    droplet.dxdt()
}

#[pyfunction]
pub fn get_initial_state(solution_string: String, environment:(f64,f64,f64), suspension_string: String, suspension_radius:f64, radius:f64,solute_concentration:f64,particle_concentration:f64)->Vec<f64>{
    let solution = Solution::get(solution_string);
    let suspension = Suspension::get(suspension_string,suspension_radius);
    let environment = atmosphere(environment.0,environment.1,environment.2);
    Droplet::new(solution,suspension,environment,radius,solute_concentration,particle_concentration).get_state()
}

#[pymodule]
fn rust_SADKAT(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(y_prime, m)?)?;
    m.add_function(wrap_pyfunction!(get_initial_state, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests{
    use crate::droplet::Droplet;
    use crate::environment::atmosphere;
    use crate::solution::silica;
    use crate::solution_definitions::aqueous_NaCl;
    use super::*;
    #[test]
    fn creating_droplet(){
        let droplet = Droplet::new(aqueous_NaCl(),silica(90e-9),atmosphere(293.0,0.45,0.0),30e-6,0.0,0.0);
        println!("{:?}",droplet.dxdt())
    }
}
