# Designed by: Florian Trocker, Olaf Teichert (FTM, Technical University of Munich, TUM CREATE Singapore)
#-------------
# Created on: 02.09.2020
# ------------
# Version: Python 3.7, Spyder 4.0.1
# -------------
# Description: 
#   In this function the charging algorithm of the the SES is implemented. 
# -------------
# Input: 
#   lim, size, time, Demand
# ------------
# Output: 
#   Battery, Grid, soc
# ------------

# %% Import libraries
import config as cf
import numpy as np

# Algorithm for charging and discharging the SES
def prescient(lim, size, time, Demand):
    max_char_pow = size * cf.Crate_max #in kW
    max_dischar_pow = size * cf.Crate_min# in kW
    
    Battery = np.zeros(len(Demand)) #power from and to battery in kW
    soc =  np.full(len(Demand),cf.soc_max) #soc
    for i in range(0,len(Demand),90):
        period_Demand = Demand[i:i+90]
        dur = len(period_Demand)
        mean_Demand = np.mean(period_Demand)
        
        if mean_Demand>lim and soc[i-1]>cf.soc_min: #Discharge battery
            myeta = 1/cf.eta
            P_requested = (lim - mean_Demand) * dur / sum(period_Demand>0) # Requested peak shaving power
            P_soc_max = (cf.soc_min-soc[i-1])*size/(dur/360)*cf.eta # Maximum power without violating min. SOC limit
            Pbat = max(P_requested, max_dischar_pow, P_soc_max) # Allowed battery power
            Battery[i:i+dur] = np.maximum(-period_Demand, np.full(dur, Pbat)) #Prevent feeding energy back into the grid
        elif mean_Demand < lim and soc[i-1]<cf.soc_max:
            myeta = cf.eta
            P_allowed = lim - mean_Demand # Allowed charging power
            P_soc_max = (cf.soc_max-soc[i-1])*size/(dur/360)/cf.eta # Allowed charging power without violating max. SOC limit
            Pbat = min(P_allowed, max_char_pow, P_soc_max) #Allowed battery power
            Battery[i:i+dur] = np.full(dur, Pbat)   
        else: myeta = 0
        
        soc[i:i+dur] = soc[i-1] + myeta*np.cumsum(Battery[i:i+dur]/360/size)
        
    Grid = Demand + Battery 
    
    # #Catch configurations that can't fully recharge their batteries
    if any(soc)<cf.soc_min or soc[-1]<cf.soc_max:
        Battery = np.full(len(Demand),np.nan)
        Grid = np.full(len(Demand),np.nan)
        soc = np.full(len(Demand),np.nan)
    
    return(Battery, Grid, soc)
