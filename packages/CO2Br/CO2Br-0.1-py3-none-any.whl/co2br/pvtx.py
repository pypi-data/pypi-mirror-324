# import sys, os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from co2br.solubility import SpeciesInfo

def _iapws97(P, T): # P:MPa; T:K
    T = T
    R = 0.461526 # specific gas constant -> kJ kg^-1 K^-1

    pi = P/16.53; g = 1386./T # non-dimensional pressure and temperature 
    iapws_n = np.array([0.14633, -0.84548, -3.7564, 3.3855, -0.95792, 0.15772, -1.6616e-2, 8.1215e-4, 2.8319e-4, -6.0706e-4, -1.8990e-2, 
                        -3.25297e-2, -2.1842e-2, -5.2838e-5, -4.7184e-4, -3.00e-4, 4.7661e-5, -4.4142e-6, -7.2695e-16, -3.1679e-5, -2.8270e-6, 
                        -8.5205e-10, -2.2425e-6, -6.5171e-7, -0.14342e-12, -4.0517e-7, -1.2734e-9, -1.7425e-10, -6.8762e-19, 1.4478e-20, 
                        2.6336e-23, -1.1928e-23, 1.8228e-24, -9.3537e-26])
    iapws_i = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 8, 8, 21, 23, 
                    29, 30, 31, 32])
    iapws_j = np.array([-2, -1, 0, 1, 2, 3, 4, 5, -9, -7, -1, 0, 1, 3, -3, 0, 1, 3, 17, -4, 0, 6, -5, -2, 10, -8, -11, -6, -29, -31, -38, 
                    -39, -40, -41])
    
    if isinstance(P, np.ndarray):
        gp = -np.sum(iapws_n*iapws_i*(7.1-pi[:,..., np.newaxis])**(iapws_i-1) * (g-1.222)**(iapws_j), axis=-1)
        gpp = np.sum(iapws_n*iapws_i*(iapws_i-1)*(7.1-pi[:,..., np.newaxis])**(iapws_i-2) * (g-1.222)**(iapws_j), axis=-1)
        # spv = R*T/(P/10) * pi*(-np.sum(iapws_n*iapws_i*(7.1-pi[:,..., np.newaxis])**(iapws_i-1) * (g-1.222)**(iapws_j), axis=-1))
        spv = R*T/P * pi*gp
        k = -pi*gpp/pi/gp
    else:
        gp = -np.sum(iapws_n*iapws_i*(7.1-pi)**(iapws_i-1) * (g-1.222)**(iapws_j))
        gpp = np.sum(iapws_n*iapws_i*(iapws_i-1)*(7.1-pi)**(iapws_i-2) * (g-1.222)**(iapws_j))
        spv = R*T/P * pi*gp
        k = -pi*gpp/pi/gp
    return 1e3/spv, k

def _volumetricDHlimitingslope(P, T): # P:bars; T:K
    U = np.array([3.4279e2, -5.0866e-3, 9.4690e-7, -2.0525, 3.1159e3, -1.8289e2, -8.0325e3, 4.2142e6, 2.1417]) 
    h2o, Z = _iapws97(P/10, T)
    # h2o = IAPWS97(P = P/10, T = T)
    D1000 = U[0]*np.exp(U[1]*T + U[2]*T**2)
    C = U[3] + U[4]/(U[5]+T)
    B = U[6] + U[7]/T + U[8]*T
    
    lnfunc = (B+P)/(B+1000)
    D = D1000 + C*np.log(lnfunc) # Dielectric constant of h20 (non-dimensional). 


    N0 = 6.0331415e23 # Avogadro Constant
    e = 1.60217733e-19 # Charge on Electron
    k = 1.3806505e-23 # Boltzman Constant
    e0 = 8.854e-12 # Permittivity of free space
    R = 83.1447

    A_phi = 1/3*(2.0*np.pi*N0*h2o/1000)**0.5 * (e**2/(4*np.pi*e0*D*k*T))**1.5 # osmotic coefficient #
    D_p = C/(B+P)
    Av = 4.0*R*T*3/2*A_phi*(1/D*D_p + Z/10)
    return Av, h2o

def lineardensitymodel(rs, rw, c, cs):
    return rw + (rs-rw)*c/cs

class Density:
    def __init__(self, P, T):
        # constants
        self.P = P*10; self.T = T+273.15 # pressure in bars; temperature in Kelvin
        self.mr = {"Na2SO4":3.5, "K2SO4":1.5, "MgSO4":3.3, "NaCl":6.0, "KCl":6.0, "MgCl2":2.0, "CaCl2":5.0}
        self.Mw = {"Na2SO4":142.04, "K2SO4":174.259, "MgSO4":120.336, "NaCl":58.44, 
                   "KCl":74.551, "MgCl2":95.211, "CaCl2":110.98, "h2O":18.015, "CO2":44.009} # units in g/mol; R: cc bar mol^-1 K^-1

        self.Av, self.rw = _volumetricDHlimitingslope(P=self.P, T=self.T)
        
    def _compute_viral_coefficients(self, salt): 
        '''
        computes the Infinite Dilution Apparent Molar Volume
        '''
        # Viral coefficients
        if "SO4" in salt:
            # elif salt == "Na2SO4":
            #     c = np.array([9.9663759e02, 4.2091252e-01, 0., 0., -4.7932011e-02, -2.3358147e-05, 2.9258506e-07, 0., -2.8689383e-02, 3.52766776e-03, 
            #                 1.6737932e-07, -1.0034145e-09, 0., 5.6700614e-05, -4.8130211e-06, -1.8982471e-03, 8.4674743e-06, 0., -3.4496965e-01, 4.4402252e-02,
            #                 0., 0., 0., 0.])
            if salt == "K2SO4":
                c = np.array([9.3045852e02, 5.0138960e-01, 0., 0., -3.1984451e-02, 3.2169705e-04, 0., -7.2720305e-02, -8.4771983e-04, -3.2587919e-07, 
                            0., 0., 8.8588004e-05, 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., -1.4759992e-03])
            elif salt == "MgSO4":
                c = np.array([9.5835279e02, 3.1204276e-01, 0., 0., -4.4367886e-02, -3.8269517e-05, 1.2604162e-06, -1.3437478e-01, 5.9556710e-03, 
                        1.3261864e-06, -6.4960244e-09, 0., 2.8500877e-04, -2.0109244e-05, 9.3289922e-04, 0., 0., 0., 0., 0., 0., 0., 0., 0.])

            V_mr = c[0] + c[1]*self.T + c[2]*self.T**2 + c[3]*self.T**3 + c[4]*self.P
            B0 = c[5] + c[6]*self.T + c[7]/(647.-self.T) + c[8]/(self.T-227.) + self.P*(c[9] + c[10]*self.T + c[11]*self.T**2 + c[12]/(647-self.T) + c[13]/(self.T-227.))
            B1 = c[14] + c[15]*self.T + c[16]*self.T**2 + c[17]/(647.-self.T) + self.P*(c[18] + c[19]*self.T + c[20]/(647.-self.T) + c[21]/(self.T-227.))
            C = c[22] + c[23]/(647.-self.T)      
        
        elif "Cl" in salt:
            if salt=="NaCl":
                c = np.array([1.06607098e03, -8.39622456e-03, 5.35429127e-04, 7.55373789e-07, -4.19512335e-01, 1.45082899e-03, -3.47807732e-06, 
                0., 1.10913788e-02, 1.14498252e-03, -5.51181270e-06, 7.05483955e-09, -5.05734723e-02, -1.32747828e-04, 4.77261581e-06, 
                -1.76888377e-08, 0., 6.40541237e-04, 3.07698827e-04, -1.64042763e-04, 7.06784935e-07, -6.50338372e-10, -4.50906014e-04])     

            elif salt=="KCl":
                c = np.array([2.90812061e02, 6.54111195e00, -1.61831978e-02, 1.46280384e-05, 1.41397987e01, -1.07266230e-01, 2.64506021e-04, 
                -2.19789708e-07, 3.02182158e-02, -2.15621394e-03, 9.24163206e-06, -1.10089434e-08, 2.87018859e-02, -6.73119697e-04, 1.68332473e-04,
                -7.99645640e-07, 1.11881560e-09, -6.59292385e-03, -2.02369103e-03, -1.70609099e-04, 1.00510108e-06, -1.86624642e-09, 1.91919166e-02])
            
            elif salt=="CaCl2":
                c = np.array([1.12080057e03, -2.61669538e-01, 1.52042960e-03, -6.89131095e-07, -5.11802652e-01, 2.22234857e-03, -5.66464544e-06,
                2.92950266e-09, 2.43934633e-02, -1.42746873e-03, 7.35840529e-06, -9.43615480e-09, -5.18606814e-02, -6.16536928e-05, -1.04523561e-05, 
                4.52637296e-08, -1.05076158e-10, 2.31544709e-03, -1.09663211e-03, 1.90836111e-04, -9.25997994e-07, 1.54388261e-09, -1.29354832e-02])

            elif salt=="MgCl2":
                c = np.array([1.18880927e03, -1.43194546e00, 3.87973220e-03, -2.20330377e-06, 6.38745038e00, -5.51728055e-02, 1.50231562e-04,
                -1.35757912e-07, 8.43627549e-03, 5.25365072e-03, -1.87204100e-05, 4.20263897e-08, -1.18062548e00, 6.07424747e-04, -1.20268210e-04,
                5.23784551e-07, -8.23940319e-10, 9.75167613e-03, -4.92959181e-04, -2.73642775e-04, 5.42602386e-07, -1.95602825e-09, 1.00921935e-01])

            V_mr = c[0] + c[1]*self.T + c[2]*self.T**2 + c[3]*self.T**3 + self.P*(c[4] + c[5]*self.T + c[6]*self.T**2 + c[7]*self.T**3)
            B0 = c[8]/(self.T-227.) + c[9] + c[10]*self.T + c[11]*self.T**2 + c[12]/(647.-self.T) + self.P*(
                c[13]/(self.T-227.) + c[14] + c[15]*self.T + c[16]*self.T**2 + c[17]/(647.-self.T)
            )
            B1 = 0.
            C = c[18]/(self.T-227.) + c[19] + c[20]*self.T + c[21]*self.T**2 + c[22]/(647.-self.T)
        return V_mr, B0, B1, C

    def AMV(self, salt, m):
        b = 1.2; a1 = 2.0 # prespecified from density model 

        if salt=="NaCl" or salt=="KCl":
            vc=1.0; va=1.0; zc=1; za=-1
            I = lambda x: 1/2*(vc*x*zc**2 + va*x*za**2)
 
        elif salt=="MgCl2" or salt=="CaCl2":
            vc=1.0; va=2.0; zc=2; za=-1
            I = lambda x: 1/2*(vc*x*zc**2 + va*x*za**2)

        elif salt=="K2SO4":
            vc = 2.0; va = 1.0; zc = 1; za = -2
            I = lambda x: 1/2 * (vc*x*zc**2 + va*x*za**2)

        elif salt == "MgSO4":
            vc = 1.0; va = 1.0; zc = 2.0; za = -2.0
            I = lambda x: 1/2 * (vc*x*zc**2 + va*x*za**2)

        else:
            raise Exception("Salt species should be among NaCl, KCl, CaCl2, MgCl2, K2SO4 or MgSO4")

        v = vc + va
        h = lambda x : np.log(1+b*np.sqrt(I(x)))/(2*b)
        g = lambda x: 2/(a1*I(x)**0.5)**2 * (1 - (1+a1*I(x)**0.5)*np.exp(-a1*I(x)**0.5))

        V_mr, B0, B1, C = self._compute_viral_coefficients(salt)

        if "SO4" in salt:
            R = 83.1447
        elif "Cl" in salt:
            R = 8.31447

        V0 = V_mr/self.mr[salt] - 1000/(self.mr[salt]*self.rw/1000) - v*np.abs(zc*za)*self.Av*h(self.mr[salt]) - \
            2*vc*va*self.mr[salt]*R*self.T*(B0 + B1*g(self.mr[salt]) +vc*zc*self.mr[salt]*C)
        Vphi = V0 + v*np.abs(zc*za)*self.Av*h(m) + 2*va*vc*m*R*self.T*(B0 + B1*g(m) + vc*zc*m*C)
        return Vphi
    
    def _h2OMolarVolume(self):
        iT_vec = np.array([self.T**3, self.T**2, self.T, 1, 1/self.T])
        jT_vec = np.array([self.T**3, self.T**2, 1])
        K0 = np.array([3.27225e-7, -4.20950e-4, 2.32594e-1, -4.16920e1, 5.71292e3])
        K1 = np.array([-2.32306e-10, 2.91138e-7, -1.49662e-4, 3.59860e-2, -3.55071])
        K2 = np.array([2.57241e-14, -1.24336e-11, 5.42707e-7])
        K3 = np.array([-4.42028e-18, 2.10007e-15, -8.11491e-11])

        K = np.array([K0 @ iT_vec.T, K1 @ iT_vec.T, K2 @ jT_vec.T, K3 @ jT_vec.T])

        if isinstance(self.P, np.ndarray):
            P_vec = np.repeat(self.P[:,...,np.newaxis], 4, axis=-1)
            for j in range(4):
                P_vec[:,...,j] = self.P**j
            Vw = np.tensordot(K, P_vec, axes=([0], [-1]))

        elif isinstance(self.P, float) or isinstance(self.P, int):
            P_vec = np.array([1.0, self.P, self.P**2, self.P**3])
            Vw = K @ P_vec.T
        return Vw
    
    def _CO2MolarVolume(self):
        T = np.array([self.T**2, self.T, 1.0, self.T**-1, self.T**-2])
        a = np.array([0.38384020e-3, -0.55953850, 0.30429268e3, -0.72044305e5, 0.63003388e7, -0.57709332e-6, 0.82764653e-3, 
                      -0.43813556, 0.10144907e3, -0.86777045e4])
        k = a[:5]@T + (a[5:10]@T)*self.P
        Vw = self._h2OMolarVolume()
        return Vw*(1+k) 
    
    def MAMV(self, m): # Mean Apparent Molar Volume
        V_phi_mean = []
        for salt, ml in m.items():
            if ml !=0:
                V_phi_mean.append(self.AMV(salt, ml)*ml)
            else:
                continue
        V_phi_mean = np.array(V_phi_mean)
        V_mean = np.sum(V_phi_mean/sum(m.values()), axis=0)
        return V_mean

    def BrineDensity(self, m, mco2=None):
        if not bool(m) or all(val==0 for val in m.values()):
            rho_br = self.rw
            V_mean = 0

        else:
            V_mean = self.MAMV(m)
            enum = np.array([m[k]*self.Mw[k] for k, _ in m.items()]).sum()
            rho_br = (1000 + enum)*self.rw*1e-3/(1000 + sum(m.values())*V_mean*self.rw*1e-3)*1000

        if mco2 is not None:
            S = SpeciesInfo(m)
            xco2, xions, _ = S.info(mco2)
            V_co2 = self._CO2MolarVolume()
            V_mean = xions*V_mean + xco2*V_co2
            enum = np.array([m[k]*self.Mw[k] for k, _ in m.items()]).sum() + mco2*self.Mw["CO2"]
            rho_co2br = (1000 + enum)*self.rw*1e-3/(1000 + (sum(m.values())+mco2)*V_mean*self.rw*1e-3)*1000
            return rho_co2br, rho_br, self.rw
        
        else:
            return rho_br, self.rw