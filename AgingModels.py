# Designed by: Florian Trocker, Olaf Teichert (FTM, Technical University of Munich, TUM CREATE Singapore)
#-------------
# Created on: 02.09.2020
# ------------
# Version: Python 3.7, Spyder 4.0.1
# -------------
# Description: 
#   This script is used to define the function for the ageing model of the SES
#-------------
# Input: 
#   time, Battery, soc, size
# ------------
# Output: 
#   t_eol
# ------------

# %% Import libraries

import config as cf
import numpy as np

# Linear aging model
def linear(time, Battery, soc, size):    
    FEC = np.trapz(abs(Battery),time)/3600/size/2
    n_days = (time[-1]-time[0])/3600/24        
    nperday = FEC/n_days 
    
    t_eol = cf.nmax/(cf.nmax/cf.tmax+nperday)
    
    return t_eol/365
    