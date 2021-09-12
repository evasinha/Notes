"""
Python modules for aggregating an ensemble of across year mean files, 
and writing output netcdf file
"""

import os
import numpy as np
import pandas as pd
import xarray as xr
from optparse import OptionParser

from plotdailymean import plot_timeseries
from writeoutfile import write_netcdf_output

__author__ = 'Eva Sinha'
__email__  = 'eva.sinha@pnnl.gov'

parser = OptionParser();

parser.add_option("--crop", dest="crop", default="", \
                  help="Modeled crop name")
parser.add_option("--outdir", dest="outdir", default="", \
                  help="Directory where ELM ensemble files containing across year mean are stored")
parser.add_option("--nsamples", dest="nsamples", default="", \
                  help="Number of parameters samples considered in the ensemble")
parser.add_option("--caseid", dest="caseid", default="", \
                  help="Case name")
parser.add_option("--fnamepre", dest="fnamepre", default="", \
                  help="file name prefix for saving plots")

(options, args) = parser.parse_args()
#----------------------------------------------------------

# Read names of all NetCDF files
fnames = []
for ind in range(1, int(options.nsamples)+1):
    fnames.append(options.outdir + options.fnamepre + '/indiv_ens_member/' + options.caseid + '_mean_across_years_' + str(ind) + '.nc')
    
# Open a multiple netCDF data file and load the data into xarrays
with xr.open_mfdataset(fnames, concat_dim='ensemble', combine='nested') as ds:

    # Reorder dimensions
    ds = ds.transpose('dayofyear', 'ensemble')

    # Assign coordinates to ensemble
    ds = ds.assign_coords(ensemble=range(1, int(options.nsamples)+1))

    # Save output xarray as a netcdf file
    outfname = options.caseid + '_mean_across_years.nc'
    write_netcdf_output(ds, options.fnamepre, filename=outfname)
                                
# Conversion constant
CONV_SEC_DAY    = 1 / (24 * 60 * 60)

# List of variable names that we want to keep
varnames=['GPP', 'NPP', 'NEE', 'ER']

# Create array of ylabels for each plot
ylabel = ['GPP [$gC~m^{-2}~day^{-1}$]', 'NPP [$gC~m^{-2}~day^{-1}$]',
'NEE [$gC~m^{-2}~day^{-1}$]','ER [$gC~m^{-2}~day^{-1}$]']

# Title for plot
title = options.crop

conv_factor = [CONV_SEC_DAY, CONV_SEC_DAY, CONV_SEC_DAY, CONV_SEC_DAY]

# Plot timeseries
plot_timeseries(outfname, varnames, title, ylabel, conv_factor, options.fnamepre)
print('Finished plotting')
