# Designed by: Florian Trocker, Olaf Teichert (FTM, Technical University of Munich, TUM CREATE Singapore)
#-------------
# Created on: 02.09.2020
# ------------
# Version: Python 3.7, Spyder 4.0.1
# -------------
# Definitions:
#   BLEL:   Bus-line electrification levels
#   SES:    Stationary Energy Storage
#   ter:    Terminal
#   CS:     Charging Station
#
#   all valiables with suffix '_z' consider a system without SES (e.g C_tot_z: Total costs of CS without SES)
# -------------
# Description: 
# This script is used to generate the results used in 'City-scale assessment of stationary energy storage 
# supporting end-station fast charging for different bus-fleet electrification levels' 
# The script is divided in 4 parts:
#   1. Import libraries
#   2. Import data
#   3. Generate results for all terminals and BLELs
#   4. Generate results for single terminal
#   5. Parameter sensitivity analysis for single terminal
# ------------
# Input: 
#   Input data (pickle files) with power profiles gernerated in CityMoS (Input/PowerProfile)
# ------------
# Output: 
#   Optimal parameters and costs for SES at every terminal and scenario (Results/results.csv)
#   Plots of the results
# ------------

# %% Import libraries and functions

# Import libraries
import numpy as np
import pickle
import pandas as pd
from scipy.optimize import minimize

# import self defined functions
import Objective
import config as cf
import MyPlots

# %% Import input data

Powerprofile = pickle.load(open('Input/PowerProfile','rb'))

# %% Find optimal size and limit for all terminals

df = pd.DataFrame(columns = ['terminal','BLEL','delta_t','n_chargers','opt_lim','opt_size','C_tot','C_dem','C_energy','C_bat','C_tru','C_dcdc','t_eol_bat','C_tot_z','C_dem_z','C_energy_z','C_tru_z'])

# Execute for two different peak power averaging periods
for t in [15,30]: 
    cf.delta_t = t
    # Execute for different BLEL, starting with the highest electrification level
    for BLEL in sorted(Powerprofile.keys(),reverse=True): 
        # Execute for all terminals
        for ter in Powerprofile[BLEL].keys(): 
            print (BLEL, ter) # Status update
            
            # Load data
            time = Powerprofile[BLEL][ter]['time']
            Demand = Powerprofile[BLEL][ter]['Demand']
            
            # Calculate time averaged peak power without SES
            Peakdemand_z = max([
                np.mean(Demand[n:n+cf.delta_t*6]) 
                for n in range(0,len(Demand),cf.delta_t*6)
                ]) 
            
            # Lookup TRU cost, unless the current BLEL is the highest BLEL
            if BLEL == sorted(Powerprofile.keys(),reverse=True)[0]:
                C_tru = []
                C_tru_z = []
            else:
                C_tru = float(df[
                    (df['BLEL']=='BLEL100')&
                    (df['terminal']==ter)&
                    (df['delta_t']==cf.delta_t)
                    ]['C_tru'])
                C_tru_z = float(df[
                    (df['BLEL']=='BLEL100')&
                    (df['terminal']==ter)&
                    (df['delta_t']==cf.delta_t)
                    ]['C_tru_z'])
            
            # Determine initialisation point for the optimisation
            Ebat_initial = 300 # Initial battery size in kWh, selected based on experience
            Plim_initial = 0.95*Peakdemand_z # Initial peak shaving power in kW, selected based on experience
            initials = [Plim_initial, Ebat_initial] # Initial values for optimization
            
            # Optimisation
            res = minimize(Objective.function, initials,                     
                          args = (time, Demand, C_tru, 'opt'),
                          method= 'Nelder-Mead', 
                          options={'xatol': 1, 'fatol':0.01, 'maxiter': 300})
            
            # Optimisation results
            opt_size = res.x[1] # Optimal battery size
            opt_lim = res.x[0] # Optimal peak shaving power
            
            # Calculate all cost components with SES
            C_tot,C_dem,C_energy,C_bat,C_tru,C_dcdc,t_eol_bat,Battery,Grid,soc= \
                 Objective.function([opt_lim,opt_size], time, Demand, C_tru,'full')
            
            # Calculate all cost components without SES
            C_tot_z,C_dem_z,C_energy_z,_,C_tru_z,_,_,_,_,_= \
                 Objective.function([Peakdemand_z,0], time, Demand, C_tru_z,'full')
            
            # Calculate cost reduction factor (CRF)
            CRF = 100*(C_tot_z - C_tot)/C_tot_z                 
            
            # append results to dataframe
            df = df.append({'terminal':ter,
                            'BLEL':BLEL,
                            'delta_t':t,
                            'n_chargers':Powerprofile[BLEL][ter]['Nchargers'],
                            'opt_lim':opt_lim,
                            'opt_size':opt_size,
                            'C_tot':C_tot,
                            'C_dem':C_dem,
                            'C_energy':C_energy,
                            'C_bat':C_bat,
                            'C_tru': C_tru,
                            'C_dcdc':C_dcdc,
                            't_eol_bat':t_eol_bat,                            
                            'C_tot_z':C_tot_z,
                            'C_dem_z':C_dem_z,
                            'C_energy_z':C_energy_z,
                            'C_tru_z':C_tru_z,
                            'CRF': CRF,
                            },ignore_index=True)

#Calculate share of demand charges
df['share_of_demand'] = df['C_dem']/df['C_tot']
df['share_of_demand_z'] = df['C_dem_z']/df['C_tot_z']
df = df.sort_values('BLEL')

# Save data as .csv-file
df.to_csv('Results/results.csv')

# Load default results for plots
#df = pd.read_csv('Results/results_default.csv')

# Generate result plots
MyPlots.result_plots(df)

# %% Single Terminal

# Define parameters
BLEL = 'BLEL050' #'BLEL030','BLEL050','BLEL070','BLEL080','BLEL090','BLEL100'
ter = 'ter_16009' #Terminal ID. See list(Powerprofile[BLEL].keys())
cf.delta_t = 30 #Peak power averaging period in minutes

# Load data
time = Powerprofile[BLEL][ter]['time']
Demand = Powerprofile[BLEL][ter]['Demand']

# Lookup optimal configuration
opt_size = float(df[
    (df['BLEL']==BLEL)&
    (df['terminal']==ter)&
    (df['delta_t']==cf.delta_t)
    ]['opt_size'])
opt_lim = float(df[
    (df['BLEL']==BLEL)&
    (df['terminal']==ter)&
    (df['delta_t']==cf.delta_t)
    ]['opt_lim'])

# Recalculate power curves
_,_,_,_,_,_,_,Battery,Grid,soc= \
     Objective.function([opt_lim,opt_size], time, Demand, [],'full')

# Generate power curve plot
MyPlots.power_curves_plot(Demand,Grid,Battery,soc,time,opt_lim,opt_size)

# %% Parameter sensitivity analysis for single terminal

# Generate points for contourplot
Peakdemand_z = max([
                np.mean(Demand[n:n+cf.delta_t*6]) 
                for n in range(0,len(Demand),cf.delta_t*6)
                ]) 

lim = np.append(opt_lim, np.linspace(np.mean(Demand),Peakdemand_z,50))
lim.sort()
size = np.append(opt_size, np.linspace(0,400,50))
size.sort()

# Calculate costs for contour plots
C_tot = np.zeros((len(lim),len(size)))
C_dem = np.zeros((len(lim),len(size)))
C_energy = np.zeros((len(lim),len(size)))
C_bat = np.zeros((len(lim),len(size)))
Peakdemand = np.zeros((len(lim),len(size)))
for i in range(0,len(lim)):
    for j in range(0,len(size)):
        C_tot[i,j], C_dem[i,j], C_energy[i,j], C_bat[i,j],_,_,_,_,Grid,_=\
            Objective.function([lim[i], size[j]], time, Demand, [], 'full')
        Peakdemand[i,j] = max([np.mean(Grid[n:n+cf.delta_t*6]) for n in range(0,len(Grid),cf.delta_t*6)])

# Calculate line at which peak shaving limit is exceeded
lim_exceeded = np.zeros(len(size))            
for j in range(0,len(size)):
     lim_exceeded[j] = next(lim[i] for i, P in enumerate(Peakdemand[:,j]) if 0.99*P<lim[i])

# Generate contour plot
MyPlots.contour_plots(size,lim,opt_size,opt_lim,
                      C_dem,C_energy,C_bat,C_tot,lim_exceeded)
