import xarray as xr
import numpy as np

# ---------- Read an existing surface dataset or landuse timeseries file ----------
fpath = '/compyfs/inputdata/lnd/clm2/surfdata_map/'
fname = 'surfdata_360x720cru_50pfts_simyr1850_c231117.nc'
#fname = 'landuse.timeseries_360x720cru_hist_50pfts_simyr1850-2015_c220216.nc'

ds = xr.open_dataset(fpath + fname)

#print(np.unique(ds['LONGXY'].values))
print(np.unique(ds.coords['lsmlon'].values))

# Rotate lon coordinates from [0,360] to [-180,180]
ds.coords['lsmlon'] = (ds.coords['lsmlon'] + 180) % 360 - 180
ds = ds.sortby(ds.lsmlon)

# Update value of variable lsmlon
ds['lsmlon'] = (ds['lsmlon'] + 180) % 360 - 180

print('After rotation')
print(np.unique(ds.coords['lsmlon'].values))
#print(np.unique(ds['LONGXY'].values))

# Write new surface data or landuse timeseries file
fname_new = 'surfdata_360x720cru_50pfts_simyr1850_c231219.nc'
#fname_new = 'landuse.timeseries_360x720cru_hist_50pfts_simyr1850-2015_c231205.nc'

ds.to_netcdf(path=fname_new, format='NETCDF3_CLASSIC')
