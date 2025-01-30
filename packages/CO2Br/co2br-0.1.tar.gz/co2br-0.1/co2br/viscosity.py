# import sys, os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from co2br.solubility import SpeciesInfo

class SolutionViscosity:
    def __init__(self, T, m):
        self.T = T+273.15
        self.T_vec = np.array([1, self.T, self.T**2])
        # Goldsack-Franchetto model coefficients for multi-component electrolyte brines. R. Sun et al. (2022)
        salts_coeff = {"NaCl":np.array([33.551, -0.08043, 6.700E-5, 50.179, -0.1811, 1.708E-4]),
                "KCl": np.array([16.029, -0.03887, 3.779E-5, 76.359, -0.3404, 3.793E-4]), 
                "K2SO4": np.array([58.025, -0.3143, 4.689E-4, 73.350, -0.4404, 5.767E-4]),
                "CaCl2": np.array([75.656, -0.1962, 2.074E-4, 120.86, -0.4830, 5.134E-4]), 
                "MgSO4": np.array([119.6, -0.2, 0., 50.613, -0.02886, -1.869E-4]), 
                "MgCl2": np.array([-23.041, 0.1614, -1.551E-4, -16.034, -0.00308, 7.250E-5])}
        
        salts = {k:v for k, v in salts_coeff.items() if k in m.keys()}
        salts['co2'] = np.array([4.7054, 0.06556, -1.553E-4, -61.411, 0.3973, -5.736E-4])
    
        self.gf = np.array(list(salts.values()))

        self.E = np.array(self.gf[:, :3] @ self.T_vec)
        self.V = np.array(self.gf[:, 3:] @ self.T_vec)

        self.S = SpeciesInfo(m)
        
    def h2OViscosity(self, rw):
        # reference physical quantities
        Tr = 647.096 #K
        Rr = 322.0 # kg/m3
        mur = 1e-6 # Pa s

        T_ = self.T/Tr; rho_ = rw/Rr
        Hi = np.array([1.67752, 2.20462, 0.6366564, -0.241605])
        Hij = np.array([[5.20094e-1, 2.22531e-1, -2.81378e-1, 1.61913e-1, -3.25372e-2, 0., 0.], 
                          [8.50895e-2, 9.99115e-1, -9.06851e-1, 2.57399e-1, 0., 0., 0.], 
                          [-1.08374, 1.88797, -7.72479e-1, 0., 0., 0., 0.,], 
                          [-2.89555e-1, 1.26613, -4.89837e-1, 0., 6.98452e-2, 0., -4.35673e-3], 
                          [0., 0., -2.57040e-1, 0., 0., 8.72102e-3, 0.], 
                          [0., 1.20573e-1, 0., 0., 0., 0., -5.93264e-4]])
        
        mu0 = 100*np.sqrt(T_) / np.sum(Hi/T_)

        lc_vec = np.array([(1/T_-1.)**i for i in range(0, 6)])

        if isinstance(rw, np.ndarray):
            rc_vec = np.repeat(rw[:,...,np.newaxis], 7, axis=-1)
            for j in range(rc_vec.shape[-1]):
                rc_vec[:,...,j] = (rho_ - 1)**j
            
            ej = np.matmul(rc_vec, Hij.T)
            mu1 = np.exp(rho_*np.tensordot(ej, lc_vec, axes=([-1, -1])))
        
        elif isinstance(rw, float) or isinstance(rw, int):
            rc_vec = np.array([(rho_-1.)**j for j in range(0, 7)])
            mu1 = np.exp(rho_*(lc_vec.T@(Hij@rc_vec.T)))
        
        mu_ = mu0*mu1 # non-dimensional viscosity
        mu_w = mu_*mur 
        return mu_w

    def Co2BrineViscosity(self, rw, mco2):
        mu_w = self.h2OViscosity(rw)
        Xi = self.S.species_molefractions(mco2)
        mur = np.exp(np.tensordot(Xi, self.E, axes=([0], [0]))/(1 + np.tensordot(Xi, self.V, axes=([0], [0]))))
        return mur*mu_w

    def MixtureViscosityModel(self, mu_d, mu_r, c_norm):
        R = np.log(mu_d/mu_r)
        return np.exp(-R*(1-c_norm))