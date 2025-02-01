use std::f64::consts::PI;

const STIFFNESS:f64=100.0;
const DAMPING:f64=20.0;

pub struct Mesh{
    pub(crate) positions: Vec<f64>,
    pub(crate) velocities: Vec<f64>,
    pub(crate) number:usize,
}

impl Mesh{
    pub fn new(radius:f64,number:usize)->Mesh{
        let positions = (0..number).into_iter().map(|n|{
            radius*(n+1) as f64/number as f64
        }).collect();
        Self{positions,velocities:vec![0.0;number],number}
    }
    pub fn new_from_data(positions:&[f64],velocities:&[f64],number:usize)->Mesh{
        Mesh{positions: Vec::from(positions),velocities: Vec::from(velocities),number}
    }
    pub fn get_acceleration(&self, new_radius:f64)->Vec<f64>{
        (0..self.number).into_iter().zip(&self.positions).zip(&self.velocities).map(|((n,r),v)|{
            (new_radius*(n+1) as f64/self.number as f64 - r)*STIFFNESS-v*DAMPING
        }).collect()
    }
    pub fn concentrations(&self,mass_solute:&[f64],mass_particles:&[f64],particle_density:f64)->Vec<f64>{
        let full_positions = [&[0.0],&self.positions[..]].concat();
        let boundaries = full_positions.iter().skip(1).zip(full_positions.iter());
        boundaries.zip(mass_solute).zip(mass_particles).map(|(((r1,r0),s),p)|{
            let volume = 4.0/3.0*PI*(r1.powi(3)-r0.powi(3)) - p/particle_density;
            s/volume
        }).collect()
    }
    pub fn get_volumes(&self)->Vec<f64>{
        let r0s = [&[0.0],&self.positions[..self.number-1][..]].concat();
        let r1s = &self.positions[..];
        r0s.iter().zip(r1s).map(|(r0,r1)|{
            4.0/3.0*PI*(r1.powi(3)-r0.powi(3))
        }).collect()
    }
}