use std::f64::consts::PI;
use crate::constants::SIGMA;
use crate::environment::Environment;
use crate::mesh::Mesh;
use crate::solution::{Solution,Suspension};
pub struct Droplet{
    //IMMUTABLE STATE
    solution: Solution,
    environment: Environment,
    suspension: Suspension,

    //MUTABLE STATE
    temperatures: Vec<f64>,
    mesh: Mesh,
    mass_of_solvent: f64,
    log_mass_particles:Vec<f64>,
    log_mass_solute:Vec<f64>,

    //DERIVED
    radius:f64,
    nusselt:f64,
    sherwood:f64,
    beta:f64,
    vapour_pressure:f64,
    solute_concentrations:Vec<f64>,
    particle_concentrations:Vec<f64>,
    solute_diffusion:Vec<f64>,
    viscosities:Vec<f64>,
    mass_particles:Vec<f64>,
    mass_solute:Vec<f64>,
    density:f64,
    specific_heat_capacity:f64,
}

impl Droplet{
    pub fn new(solution: Solution,suspension: Suspension,environment: Environment,radius:f64,solute_concentration:f64,particle_concentration:f64)->Self{
        let volume = 4.0/3.0*radius.powi(3)*PI;
        let particle_mass = volume*particle_concentration;
        let wet_volume = volume-particle_mass/suspension.particle_density;
        let solute_mass = wet_volume*solute_concentration;
        let mfs = solution.mfs_from_concentration(solute_concentration);
        let mass_solvent = solution.density(mfs)*wet_volume-solute_mass;
        let mesh = Mesh::new(radius,100);
        let mut log_solute_masses = Vec::new();
        let mut log_particle_masses = Vec::new();
        for layer_volume in mesh.get_volumes(){
            log_particle_masses.push((layer_volume*particle_concentration).ln());
            let dry_volume = log_particle_masses.last().unwrap().exp()/suspension.particle_density;
            log_solute_masses.push(((layer_volume-dry_volume) *solute_concentration).ln());
        }
        let T = environment.temperature;
        let N = mesh.number;
        Self::new_from_state(solution,environment,suspension,mesh,mass_solvent,vec![T;N],log_solute_masses,log_particle_masses)
    }
    pub fn new_from_state(solution:Solution, environment: Environment, suspension:Suspension,
               mesh:Mesh,mass_of_solvent:f64,temperatures:Vec<f64>,log_mass_solute:Vec<f64>,log_mass_particles:Vec<f64>)->Self{
        let mass_solute:Vec<f64> = log_mass_solute.iter().map(|m|m.exp()).collect();
        let mass_particles:Vec<f64> = log_mass_particles.iter().map(|m|m.exp()).collect();
        let average_concentrations = mesh.concentrations(&mass_solute,&mass_particles,suspension.particle_density);
        let mfss:Vec<f64> = average_concentrations.iter().map(|s|{
            solution.mfs_from_concentration(*s)
        }).collect();
        let vapour_pressure = solution.activity(*mfss.last().unwrap())*(&solution.solvent.equilibrium_vapour_pressure)(environment.temperature);
        let solute_diffusion: Vec<f64> = mfss.iter().zip(&temperatures).map(|(mfs,T)|{
            (&solution.diffusion)(*mfs,*T)
        }).collect();
        let viscosities = solute_diffusion.iter().zip(&temperatures).map(|(diffusion,T)|{
            solution.viscosity(*diffusion,*T)
        }).collect();
        let total_mass_solute:f64 = mass_solute.iter().sum();
        let total_mass_particles:f64 = mass_particles.iter().sum();
        let total_mfs = total_mass_solute / (total_mass_solute+mass_of_solvent);
        let total_density = solution.density(total_mfs);
        let volume = (total_mass_solute + mass_of_solvent)/total_density + total_mass_particles/suspension.particle_density;
        let radius = (3.0*volume/(4.0*PI)).powf(1.0/3.0);
        let knudsen = environment.mean_free_path()/radius;
        let beta = (1.0 + knudsen) / (1.0 + (4.0 / 3.0 * (1.0 + knudsen) + 0.377) * knudsen);
        let reynolds = environment.density()*2.0*radius*environment.speed/environment.dynamic_viscosity;
        let prandtl = environment.specific_heat_capacity*environment.dynamic_viscosity/environment.thermal_conductivity;
        let schmidt = environment.dynamic_viscosity/(environment.density()*(&solution.solvent.vapour_binary_diffusion_coefficient)(environment.temperature));
        let sherwood = 1.0+0.3*reynolds.sqrt()*prandtl.powf(1.0/3.0);
        let nusselt = 1.0+0.3*reynolds.sqrt()*schmidt.powf(1.0/3.0);

        let r0s = &mesh.positions[..mesh.number-1];
        let r1s = &mesh.positions[1..];
        let r03s = r0s.iter().map(|r|r.powi(3)).collect::<Vec<f64>>();
        let r04s = r0s.iter().map(|r|r.powi(4)).collect::<Vec<f64>>();
        let r13s = r1s.iter().map(|r|r.powi(3)).collect::<Vec<f64>>();
        let r14s = r1s.iter().map(|r|r.powi(4)).collect::<Vec<f64>>();
        let cs0 = 3.0*mass_solute[0]/(4.0*PI*r03s[0]);
        let cp0 = 3.0*mass_particles[0]/(4.0*PI*r03s[0]);
        let mut solute_concentrations = vec![cs0; 2];
        let mut particle_concentrations = vec![cp0; 2];
        for i in (0..mesh.number-1){
            let numerator_s = mass_solute[i+1]/PI + 4.0/3.0* solute_concentrations[solute_concentrations.len()-1]*(r03s[i]-r13s[i]);
            let denominator = r14s[i]-r04s[i]+4.0/3.0*r0s[i]*(r03s[i]-r13s[i]);
            let gradient_s = numerator_s/denominator;
            solute_concentrations.push(gradient_s*(r1s[i]-r0s[i])+solute_concentrations[solute_concentrations.len()-1]);

            let numerator_p = mass_particles[i+1]/PI + 4.0/3.0* particle_concentrations[particle_concentrations.len()-1]*(r03s[i]-r13s[i]);
            let gradient_p = numerator_p/denominator;
            particle_concentrations.push(gradient_p*(r1s[i]-r0s[i])+particle_concentrations[particle_concentrations.len()-1]);
        }
        let total_mass = total_mass_solute+total_mass_particles+mass_of_solvent;
        let density = total_mass/volume;
        let specific_heat_capacity = ((&solution.solvent.specific_heat_capacity)(*temperatures.last().unwrap())*(total_mass_solute+mass_of_solvent)+(suspension.specific_heat_capacity*total_mass_particles))/total_mass;
        Self{solute_diffusion,viscosities, mass_particles, vapour_pressure, solute_concentrations,
            environment,solution,suspension, mesh, mass_of_solvent, log_mass_particles,
            log_mass_solute, radius, nusselt, sherwood,
            temperatures, beta, particle_concentrations, mass_solute,density,specific_heat_capacity}
    }
    pub fn get_state(&self)->Vec<f64>{
        [&[self.mass_of_solvent],
            &self.temperatures[..],
            &self.log_mass_solute[..],
            &self.log_mass_particles[..],
            &self.mesh.positions[..],
            &self.mesh.velocities[..]].concat()
    }
    pub fn temperature_derivative(&self, mass_derivative:f64) -> Vec<f64> {
        let mut result = vec![0.0];
        if self.mesh.number>1{
            let position_iter = self.mesh.positions[1..].iter().zip(&self.mesh.positions);
            result.extend(self.temperatures[1..].iter().zip(&self.temperatures).zip(position_iter).map(|((t1,t0),(r1,r0))| {
                let kappa = (self.solution.solvent.thermal_conductivity)((t1 + t0)/2.0);
                let denominator = self.radius.powi(2)*(r1.powi(3)-r0.powi(3))*(r1-r0);
                let numerator = -3.0*kappa*(t1-t0)*r0.powi(2);
                numerator/denominator
            }))
        }
        let factor = 1.0/(self.specific_heat_capacity*self.density*self.radius);
        
        let conduction = 3.0*self.environment.thermal_conductivity*
            (self.environment.temperature-self.temperatures.last().unwrap())*
            self.nusselt/(self.radius);
        
        let heat = 3.0/(4.0*PI)*(&self.solution.solvent.specific_latent_heat_vaporisation)(*self.temperatures.last().unwrap())*mass_derivative/(self.radius.powi(2));
        
        let radiation = 3.0*SIGMA*(self.temperatures.last().unwrap().powi(4)-self.environment.temperature.powi(4));
        
        result[self.temperatures.len()-1] += factor*(conduction+heat+radiation);
        result
    }
    pub fn solvent_mass_derivative(&self) -> f64 {
        let d_eff = (self.solution.solvent.vapour_binary_diffusion_coefficient)(self.environment.temperature);
        let vapour_ratio = ((self.environment.pressure-self.vapour_pressure)/(self.environment.pressure-self.environment.vapour_pressure(&self.solution.solvent))).ln();
        4.0*PI*self.radius*self.environment.density()*(self.solution.solvent.molar_mass/self.environment.molar_mass)*d_eff*self.sherwood*vapour_ratio*self.beta
    }
    pub fn redistribute(&self)->Vec<(f64,f64)>{
        if self.mesh.number>1{
            let sign:Vec<f64> = self.mesh.velocities.iter().map(|v|v.signum()).collect();
            let volume_derivatives:Vec<f64> = self.mesh.positions.iter().zip(&self.mesh.velocities).map(|(r,v)|{
                4.0*PI*r.powi(2)*v
            }).collect();
            let fullness:Vec<f64> = self.particle_concentrations.iter().map(|c|{
                (c-self.suspension.critical_volume_fraction*self.suspension.particle_density).min(0.0).powi(2)/
                    (self.suspension.maximum_volume_fraction*self.suspension.particle_density - self.suspension.critical_volume_fraction * self.suspension.particle_density)
            }).collect();

            let mut result = vec![(0.0,0.0);self.mesh.number];
            (0..volume_derivatives.len()-1).for_each(|i|{
                if sign[i] < 0.0{
                    let particle_value = volume_derivatives[i] * (self.particle_concentrations[i]) - volume_derivatives[i + 1] * fullness[i];
                    let solute_value = volume_derivatives[i] * (self.solute_concentrations[i]);
                    result[i].0 += solute_value;
                    result[i + 1].0 -= solute_value;
                    result[i].1 += particle_value;
                    result[i + 1].1 -= particle_value;
                } else {
                    let particle_value = volume_derivatives[i] * self.particle_concentrations[i + 1];
                    let solute_value = volume_derivatives[i] * (self.solute_concentrations[i+1]);
                    result[i].0 += solute_value;
                    result[i + 1].0 -= solute_value;
                    result[i].1 += particle_value;
                    result[i + 1].1 -= particle_value;
                }
            });
            result
        } else {
            vec![(0.0,0.0)]
        }
    }
    fn get_gradients(&self, normalised_boundaries:&[f64])->Vec<(f64,f64)>{
        let solute_iter = self.solute_concentrations.iter().skip(2).zip(&self.solute_concentrations);
        let particle_iter = self.particle_concentrations.iter().skip(2).zip(&self.particle_concentrations);
        let boundary_iter = normalised_boundaries.iter().skip(2).zip(normalised_boundaries);
        solute_iter.zip(particle_iter).zip(boundary_iter).map(|(((s1,s0),(p1,p0)),(b1,b0))| {
            
            ((s1-s0)/(b1-b0),(p1-p0)/(b1-b0))
        }).collect()
    }
    pub fn diffuse(&self)->Vec<(f64,f64)>{
        if self.mesh.number>1{
            let boundaries = [&[0.0f64],&self.mesh.positions[..]].concat();
            let normal_boundaries = boundaries.iter().map(|r|r/self.radius).collect::<Vec<f64>>();
            let gradients = self.get_gradients(&normal_boundaries);
            let mut result = vec![(0.0,0.0);self.mesh.number];
            (0..self.mesh.number-1).for_each(|i|{
                let particle_diffusion = self.suspension.diffusion(self.viscosities[i],self.temperatures[i]);
                let solute_diffusion = self.solute_diffusion[i];
                let particle_value = 4.0*PI*self.radius*particle_diffusion*gradients[i].1*normal_boundaries[i+1].powi(2);
                let solute_value = 4.0*PI*self.radius*solute_diffusion*gradients[i].0*normal_boundaries[i+1].powi(2);
                result[i].0 += solute_value;
                result[i+1].0 -= solute_value;
                result[i].1 += particle_value;
                result[i+1].1 -= particle_value;
            });
            result
        } else {
            vec![(0.0,0.0)]
        }
    }
    pub fn mass_transport(&self)->(Vec<f64>,Vec<f64>){
        let layer_masses_iter = self.mass_solute.iter().zip(&self.mass_particles);
        let mut result_s = vec![0.0;self.mesh.number];
        let mut result_p = vec![0.0;self.mesh.number];
        self.diffuse().iter().zip(&self.redistribute()).zip(layer_masses_iter).enumerate().for_each(|(i,(((s0,p0),(s1,p1)),(s,p)))|{
            result_s[i] = if *s == 0.0{
                0.0
            } else {
                (s0+s1)/s
            };
            result_p[i] = if *p == 0.0{
                0.0
            } else {
                (p0+p1)/p
            };
        });
        (result_s,result_p)
    }
    pub fn dxdt(&self)->Vec<f64>{
        let mass_derivative = self.solvent_mass_derivative();
        let temperature_derivative = self.temperature_derivative(mass_derivative);
        let (solute_derivative,particle_derivative) = self.mass_transport();
        [vec![mass_derivative], 
            temperature_derivative,
            solute_derivative,
            particle_derivative,
            self.mesh.velocities.clone(), 
            self.mesh.get_acceleration(self.radius)].concat()
    }
}

