"""
Python modules for creating ytrain.dat for average daily outputs
from the ELM ensemble run
"""

import os
import numpy as np
import pandas as pd
import xarray as xr
from optparse import OptionParser

__author__ = 'Eva Sinha'
__email__  = 'eva.sinha@pnnl.gov'

parser = OptionParser();

parser.add_option("--datadir", dest="datadir", default="", \
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
nfiles = int(options.nsamples)

# Read ptrain data 
df_all         = np.loadtxt(options.datadir + options.fnamepre + '/ytrain.dat', dtype=np.double)
df_annual_all  = np.loadtxt(options.datadir + options.fnamepre + '/ytrain_annual.dat', dtype=np.double)
parms          = np.loadtxt(options.datadir + options.fnamepre + '/ptrain.dat', dtype=np.double)
     
# Write to output file
os.chdir(options.fnamepre)
np.savetxt('ytrain.dat', df_all[0:int(nfiles*0.8),:])
np.savetxt('yval.dat',   df_all[int(nfiles*0.8):,:])
np.savetxt('ytrain_annual.dat', df_annual_all[0:int(nfiles*0.8)])
np.savetxt('yval_annual.dat',   df_annual_all[int(nfiles*0.8):])
np.savetxt('ptrain.dat', parms[0:int(nfiles*0.8),:])
np.savetxt('pval.dat',   parms[int(nfiles*0.8):,:])
