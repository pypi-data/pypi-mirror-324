# import sys, os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from types import SimpleNamespace

class SpeciesInfo:
    def __init__(self, m):
        self.m = m
        S = IonicMolalities(m)
        self.tot_anionic_conc = S.mCl+S.mSO4; self.tot_cationic_conc = S.mK+S.mNa+S.mCa+S.mMg
        self.tot_ionic_conc = self.tot_anionic_conc + self.tot_cationic_conc

    def info(self, mco2): # mco2 : moles/kg
        xco2 = mco2/(55.51 + self.tot_ionic_conc + 2.0*mco2)
        xions = sum(self.m.values())/(55.51 + self.tot_ionic_conc + 2.0*mco2)
        xh2o = 1 - (xco2 + xions)
        return xco2, xions, xh2o

    def species_molefractions(self, mco2):
        tot_conc = 55.51 + self.tot_ionic_conc + 2.0*mco2
        xco2 = mco2/tot_conc
        mions = np.array(list(self.m.values()))
        xions = np.array([m/tot_conc for m in mions])
        if isinstance(mco2, np.ndarray):
            return np.concatenate((xions, xco2[np.newaxis,...,:]), axis=0)
        else:
            return np.hstack((xions, xco2))
        
def IonicMolalities(m):
    mK=0; mNa=0; mCa=0; mMg=0; mCl=0; mSO4=0 
    for salt, c in m.items():
        if c!=0 and salt == "KCl":
            mK += c; mCl += c
        if c!=0 and salt == "K2SO4":
            mK += 2*c; mSO4 += c
        if c!=0 and salt == "NaCl":
            mNa += c; mCl += c
        if c!=0 and salt == "CaCl2":
            mCa += c; mCl += 2*c
        if c!=0 and salt == "CaSO4":
            mCa+= c; mSO4 += c
        if c!=0 and salt == "MgCl2":
            mMg += c; mCl += 2*c
        if c!=0 and salt == "MgSO4":
            mMg += c; mSO4+= c

    return SimpleNamespace(mK=mK, mNa=mNa, mCa=mCa, mMg=mMg, mCl=mCl, mSO4=mSO4)

def _Ph2O(T):
    # computes the pure water pressure acc to the empirical model of Duan and Sun (2003)
    Pc = 220.85; Tc = 647.29
    c = np.array([-38.640844, 5.8948420, 59.876516, 26.654627, 10.637097])
    t = (T-Tc)/Tc
    P_sat = Pc*T/Tc*(1 + c[0]*(-t)**1.9 + c[1]*t + c[2]*t**2 + c[3]*t**3 + c[4]*t**4)
    return P_sat # bars

class Solubility:
    def __init__(self, P, T):
        self.T = T # Temeprature in Celcius
        self.P = P # Pressure in MPa
        self.P0 = 16.2086 - 12.1147/(1. + np.exp(0.049635*T - 2.8034))
        self.P_sat = _Ph2O(self.T+273.15)/10
        if len(self.P[self.P<self.P_sat]) !=0:
            raise Exception("Solubility can only be computed at a min pressure of {} MPa. Given pressure below saturated vapour pressure of pure H2O".format(self.P_sat))
    
    def CO2ActivityCoefficient(self, m):
        S = IonicMolalities(m)
        lamdaA, lamdaB, lamdaC, eta = -2.3447473e-3, 1.5231928, -3.0944008e2, 5.7587599e-3
        Ck, Cca, Cmg, Cso4 = 6.2753068e-01, 2.3350395, 2.1883697, 2.5412610e-01
    
        lamda = lamdaA*(self.T+273.15) + lamdaB + lamdaC/(self.T+273.15)
        return np.exp((lamda + eta*S.mCl)*(S.mNa+ Ck*S.mK+ Cca*S.mCa + Cmg*S.mMg) + Cso4*S.mSO4)

    def CO2Solubility(self, m):
        a_coeff = self.CO2ActivityCoefficient(m)
        chbp = np.array([[1.04e-7, 1.50e-8, -8.48e-11, 1.53e-13, 2.21e-7, -2.35e-7], 
                        [-0.8934504, 8.64e-3, -3.2540648e-5, -1.4988959e-8, 4.57e-2, 4.01e-5], 
                        [0.5729271, -3.3513558e-3, -8.4827891e-6, 1.52e-7, -5.7929902e-2, 3.895e-5], 
                        [1.012116, -1.5057825e-3, 1.66e-5, -1.0011081e-7, -3.9395094e-2, -1.6943612e-4], 
                        [0.6804949, 4.08e-3, 1.81e-5, -4.3441358e-8, 1.90e-2, -1.7145340e-4], 
                        [2.130724, -1.0764878e-3, 5.35e-5, -2.1669502e-7, 1.007592, 1.04e-3], 
                        [0.9707671, 2.78e-2, -8.2421283e-5, 1.23e-7, 0.8249869, 1.05E-03]])
            
        X = lambda x: x[0] + x[1]*self.T + x[2]*self.T**2 + x[3]*self.T**3 + x[4]/self.T + x[5]*np.log(self.T)

        c = np.apply_along_axis(X, 1, chbp)   

        if isinstance(self.P, np.ndarray):
            P = self.P.reshape(self.P.shape[0]*self.P.shape[1], -1)
            mco2 = np.zeros_like(P)

            idx_high = (P > self.P0)

            mco2_P0 = c[0]*self.P0**2 + c[1]*self.P0 + c[2]*self.P0*np.sin(np.pi/2*self.P0/(c[4]*self.P0+1)) + c[5]*np.log(self.P0+c[6]**2) - c[5]*np.log(c[6]**2)
            dmc = 2.0*c[0]*self.P0 + c[1] + c[2]*\
                (np.sin(np.pi/2*self.P0/(c[4]*self.P0+1)) + np.pi/2.*self.P0/(c[4]*self.P0+1)**2 * np.cos(np.pi/2*self.P0/(c[4]*self.P0+1)))
            
            mco2[idx_high] = mco2_P0 + dmc*(P[idx_high]-self.P0) + 1/c[3]*c[5]/(self.P0+c[6]**2)*P[idx_high]**c[3]/self.P0**(c[3]-1) - c[5]*self.P0/((self.P0+c[6]**2)*c[3])
            mco2[idx_high] = (mco2[idx_high]*a_coeff)


            idx_low = (P>self.P_sat) & (P<=self.P0)


            mco2[idx_low] = c[0]*P[idx_low]**2 + c[1]*P[idx_low] +\
                    c[2]*P[idx_low]*np.sin(np.pi/2*P[idx_low]/(c[4]*P[idx_low]+1)) + \
                        c[5]*np.log(P[idx_low]+c[6]**2) - c[5]*np.log(c[6]**2)
            mco2[idx_low] = (mco2[idx_low]*a_coeff)
            
            return mco2.reshape(self.P.shape)
            
        elif isinstance(self.P, float) or isinstance(self.P, int):
               
            if self.P>self.P0:
                mco2_P0 = c[0]*self.P0**2 + c[1]*self.P0 + c[2]*self.P0*np.sin(np.pi/2*self.P0/(c[4]*self.P0+1)) + c[5]*np.log(self.P0+c[6]**2) - c[5]*np.log(c[6]**2)
                dmc = 2.0*c[0]*self.P0 + c[1] + c[2]*\
                    (np.sin(np.pi/2*self.P0/(c[4]*self.P0+1)) + np.pi/2.*self.P0/(c[4]*self.P0+1)**2 * np.cos(np.pi/2*self.P0/(c[4]*self.P0+1)))
                
                mco2_h2o = mco2_P0 + dmc*(self.P-self.P0) + 1/c[3]*c[5]/(self.P0+c[6]**2)*self.P**c[3]/self.P0**(c[3]-1) - c[5]*self.P0/((self.P0+c[6]**2)*c[3])
                return mco2_h2o*a_coeff
            
            elif self.P>self.P_sat and self.P<=self.P0:
                mco2_P0 = c[0]*self.P**2 + c[1]*self.P + c[2]*self.P*np.sin(np.pi/2*self.P/(c[4]*self.P+1)) + c[5]*np.log(self.P+c[6]**2) - c[5]*np.log(c[6]**2)
                return mco2_P0*a_coeff