# Designed by: Florian Trocker, Olaf Teichert (FTM, Technical University of Munich, TUM CREATE Singapore)
#-------------
# Created on: 02.09.2020
# ------------
# Version: Python 3.7, Spyder 4.0.1
# -------------
# Description: 
#   This script is used to generate the following plots:
#   - Power curve plot
#   - Contour plot
#   - Result plot for all terminals
#-------------
# Input: 
#   results from 'Main'
# ------------
# Output: 
#   plots
# ------------

# %% Import libraries

import matplotlib.pyplot as plt
import seaborn as sn
import numpy as np
import pandas as pd
import config as cf

# %% Power curve plot

def power_curves_plot(Demand,Grid,Battery,SOC,time,opt_lim,opt_size):
    
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, constrained_layout=True, sharex='all', figsize=(16,9), gridspec_kw={'height_ratios': [3, 3, 2]})
    
    Peakdemand1 = [np.mean(Demand[n:n+cf.delta_t*6]) for n in range(0,len(Demand),cf.delta_t*6)]
    Peakdemand2 = [np.mean(Grid[n:n+cf.delta_t*6]) for n in range(0,len(Grid),cf.delta_t*6)]
    
    time_peak = [time[n]/3600 for n in range(0,len(Grid),cf.delta_t*6)]
    ax1.grid(color='gray', linestyle='-', linewidth=1)
    ax1.plot(time/3600, Demand, color = [0/255, 101/255, 189/255], linewidth=1) 
    ax1.plot(time_peak, Peakdemand1, '-', color = 'red', linewidth=1)
    ax1.plot([0,time[-1]/3600],[opt_lim, opt_lim], '--',dashes=(5, 2), color = 'forestgreen', linewidth=1)
    
    ax1.legend(['$P_{cs}$','$P_{cs,30}$','$P_{lim}$'],loc='upper right')
    ax1.set_ylabel('Power in kW')
    
    ax2.plot(time/3600, Grid,color = [231/255, 115/255, 38/255], linewidth=1)
    ax2.plot(time_peak, Peakdemand2, '-', color = 'purple', linewidth=1)
    ax2.plot(time/3600, Battery, color = 'darkgreen', linewidth=1)
    ax2.plot([0,time[-1]/3600],[opt_lim, opt_lim], '--', color = 'forestgreen',dashes=(5, 2), linewidth=1)
    
    ax2.legend(['$P_{grid}$','$P_{grid,30}$','$P_{bat}$','$P_{lim}$'],loc='upper right')
    ax2.set_ylabel('Power in kW')
    ax2.grid(color='gray', linestyle='-', linewidth=1)
    
    plt.xlim(4,123)
   
    ax3.plot(time/3600, SOC, color = 'black', linewidth=1)
    ax3.set_xlabel('Time in hours')
    ax3.set_ylabel('SOC')
    ax3.grid(color='gray', linestyle='-', linewidth=1)
 
    ax3.set_ylim([0,1])
    ax3.legend(['$SOC$'],loc='upper right')
    
# %% Contour plot
    
def contour_plots(size,lim,opt_size,opt_lim,C_dem,C_energy,C_bat,C_tot,lim_exceeded):
    
    plot_width = 255*2
    cont_len = 140*2
    font_size = 12
    
    #% cont_demand
    plt.figure(constrained_layout=True, figsize=(plot_width/72,cont_len/72))
    contourplot = plt.contourf(size,lim,C_dem/np.nanmin(C_tot))
    cbar = plt.colorbar(contourplot, format='%.3f')
    cbar.set_label('$C_{demand}$/$C^{*}_{tot}$',fontsize = font_size)
    cbar.ax.tick_params(labelsize=font_size)
    plt.xlabel('$E_{bat}$ in kWh', fontsize = font_size)
    plt.ylabel('$P_{lim}$ in kW', fontsize = font_size)
    plt.xticks(fontsize = font_size) 
    plt.yticks(fontsize = font_size) 
    plt.plot(size,lim_exceeded,'peru')
    plt.plot(opt_size,opt_lim,'o',color = 'sandybrown')
    
    #% cont_energy
    plt.figure(constrained_layout=True, figsize=(plot_width/72,cont_len/72))
    contourplot = plt.contourf(size,lim,C_energy/np.nanmin(C_tot))
    cbar = plt.colorbar(contourplot, format='%.3f')
    cbar.set_label('$C_{energy}$/$C^{*}_{tot}$',fontsize = font_size)
    cbar.ax.tick_params(labelsize=font_size)
    plt.xlabel('$E_{bat}$ in kWh', fontsize = font_size)
    plt.ylabel('$P_{lim}$ in kW', fontsize = font_size)
    plt.xticks(fontsize = font_size) 
    plt.yticks(fontsize = font_size) 
    plt.plot(size,lim_exceeded,'peru')
    plt.plot(opt_size,opt_lim,'o',color = 'sandybrown')
    
    #% cont_battery
    Cbat_upper = 3*np.nanmedian(C_bat)/np.nanmin(C_tot)
    Cbat_lower = np.nanmin(C_bat)/np.nanmin(C_tot)
    plt.figure(constrained_layout=True, figsize=(plot_width/72,cont_len/72))
    contourplot = plt.contourf(size,lim,C_bat/np.nanmin(C_tot),np.linspace(Cbat_lower, Cbat_upper, 10),extend='max')
    cbar = plt.colorbar(contourplot, format='%.3f')
    cbar.set_label('$C_{battery}$/$C^{*}_{tot}$',fontsize = font_size)
    cbar.ax.tick_params(labelsize=font_size)
    plt.xlabel('$E_{bat}$ in kWh', fontsize = font_size)
    plt.ylabel('$P_{lim}$ in kW', fontsize = font_size)
    plt.xticks(fontsize = font_size) 
    plt.yticks(fontsize = font_size) 
    plt.plot(size,lim_exceeded,'peru')
    plt.plot(opt_size,opt_lim,'o',color = 'sandybrown')

    # % cont_tot
    plt.figure(constrained_layout=True, figsize=(plot_width/72,cont_len/72))
    contourplot = plt.contourf(size,lim,C_tot/np.nanmin(C_tot),extend='max')
    cbar = plt.colorbar(contourplot, format='%.3f')
    cbar.set_label('$C_{tot}$/$C^{*}_{tot}$',fontsize = font_size)
    cbar.ax.tick_params(labelsize=font_size)
    plt.xlabel('$E_{bat}$ in kWh', fontsize = font_size)
    plt.ylabel('$P_{lim}$ in kW', fontsize = font_size)
    plt.xticks(fontsize = font_size) 
    plt.yticks(fontsize = font_size)
    plt.plot(size,lim_exceeded,'peru')
    plt.plot(opt_size,opt_lim,'o',color = 'sandybrown')

# %% Result plot for all terminals
    
def result_plots(df):
    
    plot_width = 255*2
    box_plot_len = 170*2
    font_size = 12
    
    # CRF over BLEL
    plt.figure(constrained_layout=True, figsize=(plot_width/72,box_plot_len/72))
    plt.grid(axis='y',color='gray', linestyle='-', linewidth=0.5)
    sn.boxplot(x = 'BLEL', 
               y = 'CRF', 
               linewidth = 0.5,
               color = 'aliceblue',
               flierprops={'markersize':2,'markeredgecolor': 'black'},
               showmeans=True,
               meanprops={'marker':"x",'markeredgecolor': 'black'},
               whis = (5,95),
               data = df[df['delta_t'] == 30],
               )
    plt.xticks([0,1,2,3,4,5],['30', '50', '70', '80', '90', '100'], fontsize = font_size)
    plt.yticks(fontsize = font_size)
    
    plt.xlabel('Bus-line electrification level in %', fontsize = font_size)
    plt.ylabel('CRF in %', fontsize = font_size)
    plt.yticks([0,2,4,6,8,10,12])
    
    # CRF over BLEL comparison between two peak averaging durations    
    plt.figure(constrained_layout=True, figsize=(plot_width/72,box_plot_len/72))
    plt.grid(axis='y',color='gray', linestyle='-', linewidth=0.5)
    Comparison = sn.boxplot(x = 'BLEL', 
               y = 'CRF',
               hue = 'delta_t',
               hue_order = [30,15],
               linewidth = 0.5,
               color = 'skyblue',
               flierprops={'markersize':2,'markeredgecolor': 'black'},
               showmeans=True,
               meanprops={'marker':"x",'markeredgecolor': 'black'},
               whis = (5,95),
               data = df,
               )
    plt.xticks([0,1,2,3,4,5],['30', '50', '70', '80', '90', '100'], fontsize = font_size)
    plt.yticks(fontsize = font_size)
    plt.xlabel('Bus-line electrification level in %', fontsize = font_size)
    plt.ylabel('CRF in %', fontsize = font_size)
    plt.yticks([0,2,4,6,8,10,12,14,16])
    Comparison.legend_.set_title('')
    handles, _ = Comparison.get_legend_handles_labels()
    Comparison.legend(handles,['Δt = 30 minutes', 'Δt = 15 minutes'],fontsize = font_size)
    
    # Scatter plot (CRF over number of chargers)
    plt.figure(constrained_layout=True, figsize=(plot_width/72,box_plot_len/72))
    plt.grid(axis='y',color='gray', linestyle='-', linewidth=0.5)
    plt.scatter(x='n_chargers',
                y='CRF', 
                s = 12,
                marker="o", 
                edgecolors='black', 
                c = 'aliceblue',
                data = df[df['delta_t'] == 30],
                )
    plt.xlabel('Number of chargers', fontsize = font_size)
    plt.ylabel('CRF in %', fontsize = font_size)
    plt.xticks([0,5,10,15,20,25,30], fontsize = font_size)
    plt.yticks([0,2,4,6,8,10,12])
    plt.yticks(fontsize = font_size)
    
    # Share of demand charge over BLEL
    df_modified = pd.melt(df, id_vars=['BLEL'], value_vars=['share_of_demand', 'share_of_demand_z'])
    df_modified.loc[df_modified['variable']=='share_of_demand','variable'] = 'with SES'
    df_modified.loc[df_modified['variable']=='share_of_demand_z','variable'] = 'without SES'
    
    plt.figure(constrained_layout=True, figsize=(plot_width/72,box_plot_len/72))
    plt.grid(axis='y',color='gray', linestyle='-', linewidth=0.5)
    sn.boxplot(x='BLEL', 
               y='value', 
               hue='variable',
               hue_order=['without SES','with SES'],
               linewidth = 0.5,
               flierprops={'markersize':2,'markeredgecolor': 'gray', 'linewidth':0.2},
               showmeans=True,
               meanprops={'marker':"x",'markeredgecolor': 'black'},
               whis = (5,95),
               data = df_modified,
               )
    plt.xticks([0,1,2,3,4,5],['30', '50', '70', '80', '90', '100'], fontsize = font_size)
    plt.yticks(fontsize = font_size)
    plt.xlabel('Bus-line electrification level in %', fontsize = font_size)
    plt.ylabel(r'$C_{demand}/C^*_{tot}$', fontsize = font_size)
    plt.ylim(0,0.5)
    plt.legend(ncol=1, fontsize = font_size)