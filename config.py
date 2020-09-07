# Designed by: Florian Trocker, Olaf Teichert (FTM, Technical University of Munich, TUM CREATE Singapore)
#-------------
# Created on: 02.09.2020
# ------------
# Version: Python 3.7, Spyder 4.0.1
# -------------
# Description: 
#   This script is used for the parametrisation
# ------------
# Input: 
#   -
# ------------
# Output: 
#   -
# ------------

# %%

# Cell parameters
soc_max = .9 # Upper SOC limit [Yan.2019]
soc_min = .1 # Lower SOC limit [Yan.2019]
Crate_max = 2 # Maximum charging Crate [Panasonic.2020]
Crate_min = -3 # Maximum discharge Crate [Panasonic.2020]
eta = 0.95 # Battery efficiency [He.2019]

# Aging parameters
EOL = 0.8 # EOL criterium [Schmalstieg.2014]
tmax = 15*365  # maximum calendaric life in days[Hesse.2017]
nmax = 10000 # maximum cycle life [Hesse.2017]
T_a = 300 # Ambient temperature in K [Schmalstieg.2014]
t_eol_tru = 20 # Lifetime of the transformer rectifier unit in years [Yan.2019]
t_eol_dcdc = 8 # Lifetime of the dcdc converter in years [Yan.2019]

# Cost parameters
r = 0.05 # Interest rate [Wei.2020]
c_bat = 112 # Battery cost in $/Wh [Fries.2017]
c_tru = 11.89 # Transformer rectifier unit cost in $/kVA [Yan.2019]
c_dcdc = 74.29 # DCDC converter cost in $/kW [Yan.2019]
c_energy = 0.0983 / 1.378 # Energy price in $/kWh (USEP average 2019) [EnergyMarketCompany.2020]
c_dem_contr = 8.9 / 1.378 # Contracted peak demand charge in $/kW (per month) [SPGroup.2019]
c_dem_uncontr = 13.35 / 1.378 # Contracted peak demand charge in $/kW (per month) [SPGroup.2019]
delta_t = 30 # Time delta for demand charge calculation in Minutes [SPGroup.2019]

# Selected models
agingmodel = 'linear' # aging model
algorithm = 'prescient' #algorithm

# Check ups
if soc_max-soc_min > EOL:
    print('')
    raise SystemExit('Error: soc limits too large to cycle until EOL condition')
