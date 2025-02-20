#!/usr/bin/env python3
'''
This file contains all thermodynamics calculation functions
'''
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression



def d_eff(time, MR, thickness):
    '''
    calculates the effective diffusivity
    given the time and moisture ratio
    '''
    ln_MR = np.log(MR) # get natural log of MR

    time = time * 60 # convert time from mins to secs.

    time = time.reshape(-1, 1)
    
    thickness = thickness*0.001 # convert thickness from mm to m

    half_thickness = thickness/2   # get half of the thickness

    # perform linear regression
    model = LinearRegression()
    model.fit(time, ln_MR)

    slope = model.coef_[0] # get slope of linear regression
    # print(slope)

    fitted_MR = model.predict(time)
    
    # plt.scatter(time, ln_MR, color='blue', label='Actual Data')
    # plt.plot(time, fitted_MR, color='r', label='Regression Line')
    # plt.title('Graph of ln(MR) vs Time')
    # plt.xlabel('Time(mins)')
    # plt.ylabel('Moisture Ratio (MR)')
    # plt.legend()
    # plt.grid(1)
    # plt.show()

    Deff = -(slope * 4 * (half_thickness**2))/(np.pi**2)
    return Deff


def get_activation_energy(Deff, temp):
    '''
    calculate the activation energy of a sample
    '''
    R = 8.3145 # universal gas constant

    inv_temp = 1/(temp + 273.15) # take the inverse of temperature in kelvin
    
    # get natural log of effective diffusivity
    ln_Deff = np.log(np.array(Deff))
      
    inv_temp = inv_temp.reshape(-1, 1)
    
    # perform linear regression
    model = LinearRegression()
    model.fit(inv_temp, ln_Deff)

    # fitted_Deff = model.predict(inv_temp)

    
    # plt.scatter(inv_temp, ln_Deff, color='blue', label='Actual Data')
    # plt.plot(inv_temp, fitted_Deff, color='r', label='Regression Line')
    # plt.title('Graph of ln(Deff) vs 1/T')
    # plt.xlabel('1/Temperature(1/K)')
    # plt.ylabel('ln(Deff)')
    # plt.legend()
    # plt.grid(1)
    # plt.show()

    slope = model.coef_[0]
    intercept = model.intercept_
    activation_energy = -R * slope
    return activation_energy, intercept

def get_enthalpy(Ea, temp):
    '''
    calculate enthalpy change 
    ∆H = Ea - RTa 
    '''
    R = 8.3145 # universal gas constant

    temp = temp + 273.15 # convert temperature to kelvin.
    delta_H = Ea - (R*temp)

    return delta_H

def get_entropy(lnDo, temp):
    '''
    calculate entropy change
    ∆S = R(lnDo - lnKB/hp -lnTa) 
    '''

    R = 8.3145 # universal gas constant.
    kb = 1.38 * 10**-23 # Boltzmann constant 
    hp = 6.626 * 10**-34 # Planck constant 

    temp = temp + 273.15 # convert temperature to kelvin.

    delta_S = R*(lnDo - np.log(kb/hp) - np.log(temp))

    return(delta_S)


def get_gibbs(delta_H, delta_S, temp):
    '''
    calculate gibbs free energy
    ∆G = ∆H - ∆(TS)
    '''

    temp = temp + 273.15 # convert temperature to kelvin.
    
    gibbs_free_energy = delta_H - (temp*delta_S)

    return gibbs_free_energy