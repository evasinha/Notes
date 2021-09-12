"""
Python modules for plotting time series
"""

import os
import numpy as np
import pandas as pd
import xarray as xr

__author__ = 'Eva Sinha'
__email__  = 'eva.sinha@pnnl.gov'

#----------------------------------------------------------
def write_netcdf_output(ds, dirname, filename):
    """Save output xarray as a netcdf file
    :param: ds:         input data array

    :param: dirname:    directory for writing netcdf file

    :param: filename:   name of output netcdf file

    """
    # Change directory
    if not os.path.exists(dirname):
        os.mkdir(dirname)

    os.chdir(dirname)

    if os.path.exists(filename):
        os.remove(filename)

    # Write xarray to a new NetCDF file
    ds.to_netcdf(path=filename, mode='w')

    os.chdir('../')

#----------------------------------------------------------
def write_csv_output(ds, dirname, filename):
    """Save output xarray as a csv file
    :param: ds:         input data array

    :param: dirname:    directory for writing netcdf file

    :param: filename:   name of output csv file

    """
    # Change directory
    if not os.path.exists(dirname):
        os.mkdir(dirname)

    os.chdir(dirname)

    if os.path.exists(filename):
        os.remove(filename)

    # Convert to pandas Dataframe for writing csv file
    df = ds.to_dataframe()
   
    # Drop longitude and latitude columns
    df = df.drop(['longitude', 'latitude'], axis=1)
     
    # Save to csv file
    df.to_csv(filename)
    print('Finished writing csv')

    os.chdir('../')

#----------------------------------------------------------
def write_df_to_csv(df, dirname, filename):
    """Save output pandas dataframe as a csv file
    :param: df:         input dataframe

    :param: dirname:    directory for writing netcdf file

    :param: filename:   name of output csv file

    """
    # Change directory
    if not os.path.exists(dirname):
        os.mkdir(dirname)

    os.chdir(dirname)

    if os.path.exists(filename):
        os.remove(filename)
     
    # Save to csv file
    df.to_csv(filename, index=True)
    print('Finished writing csv')

    os.chdir('../')

