import os
import sys
import matplotlib as mpl
mpl.use('Agg')
import numpy as np
import xarray as xr

__author__ = 'Eva Sinha'
__email__  = 'eva.sinha@pnnl.gov'

# ----- Open surface dataset containing irrigation fields -----
fpath   = '/compyfs/inputdata/lnd/clm2/surfdata_map/'
fname_surf_ref = 'surfdata_0.5x0.5_simyr1850_c211019.nc'
surf_data_ref = xr.open_dataset(fpath + fname_surf_ref)

# surface dataset does not have coordinates assigned to lat lon dimensions
# Assign coordinates to lat lon dimensions
surf_data_ref = surf_data_ref.assign_coords({'lsmlon': np.unique(surf_data_ref['LONGXY'])})
surf_data_ref = surf_data_ref.assign_coords({'lsmlat': np.unique(surf_data_ref['LATIXY'])})

# Convert from -180 to 180 to 0 to 360
surf_data_ref = surf_data_ref.assign_coords(lsmlon=((surf_data_ref.lsmlon + 360) % 360))
# Roll the surface dataset
surf_data_ref = surf_data_ref.roll(lsmlon = int(len(surf_data_ref['lsmlon']) / 2), roll_coords=True)

# ----- Open 50 pft surface dataset -----
fname_surf = 'surfdata_360x720cru_50pfts_simyr1850_c230615.nc'
surf_data = xr.open_dataset(fpath + fname_surf)

# Create new surface data netcdf file
fname_new = 'surfdata_360x720cru_50pfts_simyr1850_c231117.nc'

update_irrig_var = ['FIRRIG', 'FSURF', 'FGRD']

# FIRRIG(lsmlat, lsmlon)
# FSURF(lsmlat, lsmlon)
# FGRD(lsmlat, lsmlon)

for var in update_irrig_var:
  surf_data[var] = surf_data_ref[var]

# Write new surface dataset
surf_data.to_netcdf(fname_new, format='NETCDF3_64BIT') # rewrite to netcdf
