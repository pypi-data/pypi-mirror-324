use std::f64::consts::PI;
use crate::constants::K;
use crate::fit::polynomial;
use crate::solution_definitions::aqueous_NaCl;

pub struct Solute {
    pub molar_mass: f64,
    pub number_ions: i8,
    pub density: f64,
    pub refractive_index: f64,
}
pub struct Solvent{
    pub(crate) molar_mass: f64,
    pub(crate) density: Box<dyn Fn(f64) -> f64>,
    pub(crate) specific_heat_capacity: Box<dyn Fn(f64) -> f64>,
    pub(crate) specific_latent_heat_vaporisation: Box<dyn Fn(f64) -> f64>, 
    pub(crate) equilibrium_vapour_pressure: Box<dyn Fn(f64) -> f64>,
    pub(crate) vapour_binary_diffusion_coefficient: Box<dyn Fn(f64) -> f64>,
    pub(crate) surface_tension: Box<dyn Fn(f64) -> f64>,
    pub(crate) refractive_index: f64,
    pub(crate) thermal_conductivity: Box<dyn Fn(f64) -> f64>,
}

pub struct Suspension {
    pub(crate) specific_heat_capacity: f64,
    particle_radius: f64,
    pub(crate) particle_density: f64,
    pub(crate) critical_volume_fraction: f64,
    critical_shell_thickness: f64,
    pub(crate) maximum_volume_fraction: f64,
}

impl Suspension {
    pub fn diffusion(&self, viscosity:f64, temperature:f64)->f64{
        K*temperature/(6.0*PI*viscosity*self.particle_radius)
    }
    pub fn get(name:String,radius:f64)->Suspension{
        match name.as_str(){
            "silica"=>silica(radius),
            bad_suspension => {panic!("{} IS NOT A KNOWN SUSPENSION",bad_suspension)},
        }
    }
}

pub fn silica(particle_radius:f64)->Suspension{
    Suspension{
        specific_heat_capacity: 703.0,
        particle_radius,
        particle_density: 2200.0,
        critical_volume_fraction: PI/6.0,
        critical_shell_thickness: 6.0,
        maximum_volume_fraction: 1.0,
    }
}

pub struct Solution {
    pub(crate) solvent: Solvent,
    pub solute: Solute,
    pub diffusion: Box<dyn Fn(f64,f64) -> f64>,
    pub solubility_limit: f64,
    pub activity_coefficients: Vec<f64>,
    pub density_coefficients: Vec<f64>,
    pub mfs_coefficients: Vec<f64>,
}

impl Solution {
    pub fn mfs_from_concentration(&self, concentration: f64) -> f64 {
        polynomial(&self.mfs_coefficients, concentration)
    }
    pub fn density(&self, mfs: f64) -> f64 {
        polynomial(&self.density_coefficients, mfs.sqrt())
    }
    pub fn activity(&self, mfs: f64) -> f64 {
        polynomial(&self.activity_coefficients, mfs)
    }
    pub fn concentration(&self, mfs: f64) -> f64 {
        self.density(mfs) * mfs
    }
    pub fn viscosity(&self, diffusion: f64,temperature:f64) -> f64 {
        diffusion/(K*temperature)
    }
    pub fn refractive_index(&self, mfs: f64, temperature: f64) -> f64 {
        let solution_d = self.density(mfs);
        let solute_d = self.solute.density;
        let solute_ri = self.solute.refractive_index;
        let solvent_d = (self.solvent.density)(temperature);
        let solvent_ri = self.solvent.refractive_index;
        ((1.0 + 2.0 * solution_d * (((solute_ri.powi(2) - 1.0) * mfs) / ((solute_ri.powi(2) + 2.0) * solute_d)
                    + ((1.0 - mfs) * (solvent_ri.powi(2) - 1.0))
                        / (solvent_d * (solvent_ri.powi(2) + 2.0))
        )) / (1.0 - solution_d * (((solute_ri.powi(2) - 1.0) * mfs) / ((solute_ri.powi(2) + 2.0) * solute_d)
                        + ((1.0 - mfs) * (solvent_ri.powi(2) - 1.0))
                            / (solvent_d * (solvent_ri.powi(2) + 2.0)))))
            .sqrt()
    }
    pub fn get(name:String)->Solution{
        match name.as_str(){
            "aqueous_NaCl"=>aqueous_NaCl(),
            bad_solution => {panic!("{} IS NOT A KNOWN SOLUTION",bad_solution)},
        }
    }
}
