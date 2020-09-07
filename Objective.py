# Designed by: Florian Trocker, Olaf Teichert (FTM, Technical University of Munich, TUM CREATE Singapore)
#-------------
# Created on: 02.09.2020
# ------------
# Version: Python 3.7, Spyder 4.0.1
# -------------
# Description:
# The objective function evaluates the system costs for the given battery size, 
# peak shaving power and power profile. The costs for the Transformer Rectifier
# Unit (TRU) from the highest BLEL are used, unless the current configuration is
# the configuration with the highest BLEL
# -------------
# Input: 
#   param, time, Demand, C_tru, output
# ------------
# Output: 
#   C_tot, C_dem, C_energy, C_bat, C_tru, C_dcdc, t_eol_bat, Battery, Grid, soc
# ------------

# %% Import libraries
import config as cf
import numpy as np
import AgingModels
import Algorithms

# Objective function
def function(param, time, Demand, C_tru, output):
    
    lim = param[0]
    size = param[1]
    
    #Catch unvalid limits and sizes
    Peakdemand_z = max([
                np.mean(Demand[n:n+cf.delta_t*6]) 
                for n in range(0,len(Demand),cf.delta_t*6)
                ]) 
    if (lim<0 or lim>Peakdemand_z or size<0):
        Battery = [np.nan]
        Grid = [np.nan]
        soc = [np.nan]
        t_eol_bat = np.nan  
        C_bat = np.nan
        C_dcdc = 0.0
    elif size == 0:
        Battery = np.zeros(len(Demand))
        Grid = Demand
        soc = np.full(len(Demand),cf.soc_max)  
        t_eol_bat = np.nan          
        C_bat = 0.0      
        C_dcdc = 0.0
    else:
        # Determine battery and grid power for current limit
        Battery, Grid, soc = Algorithms.prescient(lim, size, time, Demand)

        # Calculate battery life
        t_eol_bat = AgingModels.linear(time, Battery, soc, size)
        
        # Calculate battery cost
        q_bat = (cf.r*(1+cf.r)**t_eol_bat)/((1+cf.r)**t_eol_bat-1)
        C_bat = cf.c_bat * size * q_bat
        
        # Calculate dcdc costs
        q_dcdc = (cf.r*(1+cf.r)**cf.t_eol_dcdc)/((1+cf.r)**cf.t_eol_dcdc-1)
        C_dcdc = abs(cf.Crate_min) * size * cf.c_dcdc * q_dcdc
       
    # Calculate TRU costs if no TRU cost is provided
    if not(C_tru):
        q_tru = (cf.r*(1+cf.r)**cf.t_eol_tru)/((1+cf.r)**cf.t_eol_tru-1)
        C_tru = max(Grid) * cf.c_tru * q_tru

    # Calculate peak demand cost
    Peakdemand = max([
        np.mean(Grid[n:n+cf.delta_t*6]) 
        for n in range(0,len(Grid),cf.delta_t*6)]) #Peak demand power
    C_dem = (cf.c_dem_contr * min(lim,Peakdemand) + 
             cf.c_dem_uncontr * max(0,Peakdemand-lim)) * 12 #Peak demand cost
    
    # Calculate energy costs
    n_days = (time[-1]-time[0])/3600/24
    E_annual = sum(Grid)*10/3600*365/n_days # energy demand
    C_energy = cf.c_energy * E_annual
    
    # Calculate total costs
    C_tot = C_bat + C_dcdc + C_tru + C_energy + C_dem
    
    if output == 'opt':
        return(C_tot)
    elif output == 'full':
        return(C_tot, C_dem, C_energy, C_bat, C_tru, C_dcdc, t_eol_bat, Battery, Grid, soc)