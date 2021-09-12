"""
Python modules for plotting time series
"""

import os
import matplotlib as mpl
mpl.use('Agg')
import numpy as np
import pandas as pd
import xarray as xr

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter

__author__ = 'Eva Sinha'
__email__  = 'eva.sinha@pnnl.gov'

plt.rc('figure', titlesize=20)
plt.rc('legend', fontsize=20)
plt.rc('axes',   labelsize=20, titlesize=20)
plt.rc('xtick',  labelsize=20)
plt.rc('ytick',  labelsize=20)

#----------------------------------------------------------
def plot_timeseries(fpath, varnames, title, ylabel, conv_factor, fname):
    """Plot timeseries from input xarray
    :param: fpath:         path to input netcdf file for plotting

    :param: varnames:      list of variable names of interest

    :param: title:         variable title for plotting

    :param: ylabel:        variable ylabel for plotting

    :param: conv_factor:   conversion factor for each variable

    :param: fname:         file name prefix
    """

    # Plot model and observations
    parameters = {'figure.titlesize':20,
                  'legend.fontsize': 20,
                  'axes.labelsize' : 20,
                  'axes.titlesize' : 20,
                  'xtick.labelsize': 20,
                  'ytick.labelsize': 20,
                  'font.size'      : 20,
                  'figure.figsize' : (11, 8.5)}
    
    plt.rcParams.update(parameters)
    # plt.rcParams.keys()
    
    # Change directory    
    os.chdir(fname)
  
    # Open netcdf file for plotting
    ds = xr.open_dataset(fpath)

    for ind, var in enumerate(varnames):

        # Subset variable for plotting
        ds_plot = ds[var]
        
        # Scale by factor
        ds_plot = ds_plot / conv_factor[ind]

        # Model average across all ensemble members
        ds_avg = ds_plot.mean('ensemble')
        
        fig, ax = plt.subplots()
        plt.plot(ds_plot, color='lightgrey', linewidth=0.2)
        plt.plot(ds_avg,  color='black', linewidth=1.0, label='Model mean')
        plt.title(title)
        plt.ylabel(ylabel[ind])
        plt.legend(loc='upper left')
 
        # Define the month format
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))
        plt.gca().xaxis.set_major_formatter(DateFormatter('%d-%b'))
            
        plt.savefig(fname + '_' +  var + '.pdf', bbox_inches='tight') 

        plt.close(fig=None)
#----------------------------------------------------------
