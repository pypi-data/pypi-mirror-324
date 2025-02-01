use std::f64::consts::PI;
use crate::constants::GAS_CONSTANT;
use crate::solution::Solvent;

pub struct Environment {
    pub(crate) molar_mass:f64,
    pub(crate) pressure: f64,
    pub(crate) temperature: f64,
    pub relative_humidity: f64,
    pub(crate) thermal_conductivity: f64,
    pub dynamic_viscosity: f64,
    pub speed: f64,
    pub specific_heat_capacity:f64
}

impl Environment {
    pub fn density(&self) -> f64 {
        (1e-3*self.molar_mass) * self.pressure / (GAS_CONSTANT * self.temperature)
    }
    pub fn vapour_pressure(&self,solvent: &Solvent) -> f64 {
        self.relative_humidity * (solvent.equilibrium_vapour_pressure)(self.temperature)
    }
    pub fn mean_free_path(&self) -> f64 {
        self.dynamic_viscosity / self.density() * (PI * 1e-3*self.molar_mass / (2.0*GAS_CONSTANT * self.temperature)).sqrt()
    }
    pub fn wet_bulb_temperature(&self)->f64{
        let celsius = self.temperature - 273.15;
        let rh = self.relative_humidity * 100.0;
        celsius * (0.151977 * (rh + 8.313659).sqrt()).atan() + 0.00391838 * rh.powi(3).sqrt() * (
            0.023101 * rh).atan() - (rh - 1.676331).atan() + (celsius + rh).atan() - 4.686035 + 273.15
    }
}

pub fn atmosphere(temperature:f64,relative_humidity:f64,speed:f64)->Environment {
    Environment{
        molar_mass: 28.9647,
        pressure: 101325.0,
        temperature,
        relative_humidity,
        specific_heat_capacity:0.7175,
        thermal_conductivity: 2.5e-2,
        dynamic_viscosity: 18.13e-6,
        speed
    }
}