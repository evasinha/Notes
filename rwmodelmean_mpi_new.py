"""
Python modules for reading an ensemble of files, 
estimating across year mean, and writing output netcdf file
"""

import os, time
import numpy as np
import pandas as pd
import xarray as xr
from mpi4py import MPI
from optparse import OptionParser

from plotdailymean import plot_timeseries
from estaverage import estimate_daily_average_across_years
from writeoutfile import write_netcdf_output

__author__ = 'Eva Sinha'
__email__  = 'eva.sinha@pnnl.gov'

parser = OptionParser();

parser.add_option("--plist_file", dest="plist_file", default="", \
                  help="File containing parameter name and pft")
parser.add_option("--rundir", dest="rundir", default="", \
                  help="Directory where ELM ensemble outputs are stored")
parser.add_option("--nsamples", dest="nsamples", default="", \
                  help="Number of parameters samples considered in the ensemble")
parser.add_option("--caseid", dest="caseid", default="", \
                  help="Case name")
parser.add_option("--yr_start", dest="yr_start", default=2000, \
                  help="Start year for reading ELM model outputs")
parser.add_option("--yr_end", dest="yr_end", default=2005, \
                  help="Last year for reading ELM model outputs")
parser.add_option("--fnamepre", dest="fnamepre", default="", \
                  help="file name prefix for saving plots")

(options, args) = parser.parse_args()

#----------------------------------------------------------
def read_output_data(plist_file, rundir, nsamples, caseid, yr_start, yr_end, varnames, fnamepre):
    """Read ELM model output for all ensemble members for specified case and year range and subset for variables
    :param: rundir:     path to the run directory
    
    :param: caseid:     case name
    
    :param: yr_start:   first year for reading data
    
    :param: yr_end:     last year for reading data
    
    :param: varnames:   list of variable names of interest
   
    :param: fnamepre:   file name prefix for saving plots 
    """

    comm=MPI.COMM_WORLD
    rank=comm.Get_rank()
    size=comm.Get_size()

    # Read names of output variables and conversion factor
    calib_var = pd.read_csv('calib_var.csv', comment='#')

    # File containing parameter name and pft
    #plist_path = '/home/ac.eva.sinha/OLMT/' 
    #plist_file = 'parm_list_miscanthus'

    # Obtain the parameter names
    pnames=[]
    ppfts=[]
    #pfile = open(plist_path + plist_file, 'r')
    pfile = open(plist_file, 'r')
    nparms = 0
    for s in pfile:
        pnames.append(s.split()[0])
        ppfts.append(s.split()[1])
        nparms = nparms+1
    pfile.close()

    if (rank == 0):  #master
      n_done = 0
   
      for n_job in range(1,size):
        comm.send(n_job, dest=n_job, tag=1)
        comm.send(0,     dest=n_job, tag=2)
        time.sleep(1)
       
      for n_job in range(size, int(nsamples)+1):
        process = comm.recv(source=MPI.ANY_SOURCE, tag=3)
        thisjob = comm.recv(source=process,        tag=4)
        
        n_done = n_done+1
        comm.send(n_job, dest=process, tag=1)
        comm.send(0,     dest=process, tag=2)
       
      while(n_done < int(nsamples)):
        process = comm.recv(source=MPI.ANY_SOURCE, tag=3)
        thisjob = comm.recv(source=process,        tag=4)
    
        n_done = n_done+1
        comm.send(-1, dest=process, tag=1)
        comm.send(-1, dest=process, tag=2)
      
      MPI.Finalize()

    else:
  
      status=0
      while status == 0:
        myjob  = comm.recv(source=0, tag=1)
        status = comm.recv(source=0, tag=2)
    
        if (status == 0):

          dirname = 'g' + str(100000+myjob)[1:]
          filepath = rundir + '/' + dirname
        
          # Read names of all NetCDF files within the given year range
          fnames = []
          for yr in range(int(yr_start), int(yr_end)+1):
             fnames.append(filepath + '/' + caseid + '.elm.h0.' + str(yr) + '-01-01-00000.nc')
        
          # Open a multiple netCDF data file and load the data into xarrays
          with xr.open_mfdataset(fnames, concat_dim='time') as ds:
    
            # Only keep select variables in the data array
            ds = ds[varnames]
            
            # Drop landgrid dimension
            ds = ds.isel(lndgrid=0)

            # Estimate average across years for each day of the year
            ds = estimate_daily_average_across_years(ds)
    
            # Save output xarray as a netcdf file
            outfname = caseid + '_mean_across_years_' + str(myjob) + '.nc'
            print(outfname)
            write_netcdf_output(ds, fnamepre, filename=outfname)
  
          # Create empty panda series
          df_all        = pd.Series(dtype = 'float64')

          for index, row in calib_var.iterrows():
            # Convert to pandas dataframe and then pivot the data
            df = ds[row['variable']].to_dataframe().unstack(level=-1)*row['daily_multi_factor']

            # Estimate annual average
            df_annual = df.mean()*(row['annual_multi_factor']/row['daily_multi_factor'])

            if (len(df_all.index) == 0):
              df_all        = df
              df_annual_all = pd.Series([df_annual])
            else:
              # Combine by concatinating along columns
              df_all        = pd.concat([df_all, df],               axis=0, ignore_index=True)
              df_annual_all = df_annual_all.append(pd.Series([df_annual]), ignore_index=True)

          # Reshape single columm to single row and append data to file
          f1 = open(fnamepre + '/ytrain.dat', 'ab')
          df_all = df_all.to_numpy()
          np.savetxt(f1, df_all.reshape(1,len(df_all)))
          f1.close()

          f2 = open(fnamepre + '/ytrain_annual.dat', 'ab')
          df_annual_all = df_annual_all.to_numpy()
          np.savetxt(f2, df_annual_all.reshape(1,len(df_annual_all)))
          f2.close()
  
          # Numpy array for saving parameter values
          parms = np.zeros([nparms], float)

          # Open netcdf parameter file
          pfname = filepath + '/clm_params_' + str(dirname[1:6]) + '.nc'
          print(dirname)
          print(pfname)
          with xr.open_dataset(pfname, decode_times=False) as mydata:
    
            for pnum, pname in enumerate(pnames):
              parms[pnum] = mydata[pname][int(ppfts[pnum])]

          # Reshape single columm to single row and append data to file
          f=open(fnamepre + '/ptrain.dat', 'ab')
          np.savetxt(f, parms.reshape(1,len(parms)))
          f.close()

          comm.send(rank,  dest=0, tag=3)
          comm.send(myjob, dest=0, tag=4)

      MPI.Finalize()

#----------------------------------------------------------
# List of variable names that we want to keep
varnames=['GPP', 'NPP', 'NEE', 'ER', 'AR', 'GR', 'HR', 'MR', 'XR', 'XSMRPOOL', 'TLAI', 'FPG', 'DMYIELD', 'BTRAN', 'FERT', 'EFLX_LH_TOT', 'FSH', 'QSOIL', 'QVEGE', 'QVEGT', 'TBOT', 'RAIN', 'SNOW']

# Read ELM model output for specified case and year range and subset for variables
read_output_data(options.plist_file, options.rundir, options.nsamples, options.caseid, options.yr_start, options.yr_end, varnames, options.fnamepre)

