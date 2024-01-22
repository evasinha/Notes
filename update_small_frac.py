import numpy as np
import xarray as xr
import sys
import warnings
warnings.filterwarnings("ignore")

__author__ = 'Eva Sinha'
__email__  = 'eva.sinha@pnnl.gov'

# Based on normalizencheck_landuse in E3SM/components/elm/tools/mksurfdata_map/src/mksurfdat.F90
# and remove_small_cover in E3SM/components/elm/tools/mksurfdata_map/src/mkutilsMod.F90

# ---------- Read an existing surface dataset of landuse timeseries file ----------
fpath = '/compyfs/inputdata/lnd/clm2/surfdata_map/'
fname = 'surfdata_360x720cru_50pfts_simyr1850_c231219.nc'

too_small = 1e-10

#ds    = xr.open_dataset(fpath + fname)	
ds    = xr.open_dataset(fname)	

# Subset variable
pct_cft     = ds['PCT_CFT']
pct_crop    = ds['PCT_CROP']
pct_natveg  = ds['PCT_NATVEG']
pct_wetland = ds['PCT_WETLAND']
pct_lake    = ds['PCT_LAKE']
pct_glacier = ds['PCT_GLACIER']
pct_urban   = ds['PCT_URBAN']

# Create a new multiindex coordinate
pct_cft     = pct_cft.stack(grid=['lsmlat','lsmlon'])
pct_crop    = pct_crop.stack(grid=['lsmlat','lsmlon'])
pct_natveg  = pct_natveg.stack(grid=['lsmlat','lsmlon'])
pct_wetland = pct_wetland.stack(grid=['lsmlat','lsmlon'])
pct_lake    = pct_lake.stack(grid=['lsmlat','lsmlon'])
pct_glacier = pct_glacier.stack(grid=['lsmlat','lsmlon'])
pct_urban   = pct_urban.stack(grid=['lsmlat','lsmlon'])

# ----- Iterate over the new grid dimension -----
for coor, pct_cft_sub in pct_cft.groupby('grid'):

  # Subset pct_crop  using grid coordiantes
  pct_crop_sub    = pct_crop.sel(grid = coor)
  pct_natveg_sub  = pct_natveg.sel(grid = coor)
  pct_wetland_sub = pct_wetland.sel(grid = coor)
  pct_lake_sub    = pct_lake.sel(grid = coor)
  pct_glacier_sub = pct_glacier.sel(grid = coor)
  pct_urban_sub   = pct_urban.sel(grid = coor)

  # Defining proportion of each crop type (pctcft) within the grid crop area (pctcrop)
  cropwts = ((pct_cft_sub * pct_crop_sub)/ (100*100))

  is_small = cropwts.where((cropwts < too_small) & (cropwts > 0))

  # Loop through grids which have cropwts for cfts below the threshold
  if( np.isnan(np.nanmax(is_small.values)) == False):
    print(coor)
    print('pct_cft_sub ', pct_cft_sub.values)
    print('pct_crop_sub ', pct_crop_sub.values)
    print('is_small ', is_small.values)

    if (np.count_nonzero(~np.isnan(is_small.values)) == np.count_nonzero(pct_cft_sub)):
      # If all CFTs are either 0 or small, then set PCT_CROP wil be set to 0
      print('all CFTs are either 0 or small')
      pct_crop.loc[dict(grid = coor)] = 0
    else:
      # If there are some big CFTs, then PCT_CFT and PCT_CROP are adjusted
      # PCT_CFT will be set to 0 for the small elements, and renormalizing for other elements
      print('there are some big CFTs')
      correction = 0
      for i in range(np.size(pct_cft_sub.values)):
        if(~np.isnan(is_small.values[i])):
          correction = correction + ((pct_cft_sub[i] * pct_crop_sub) / (100*100))
          pct_cft.loc[dict(grid = coor)][i] = 0
          print(i, correction)
          print('PCT_CFT after correction', pct_cft.loc[dict(grid = coor)])

      # Update PCT_CROP and PCT_CFT
      pct_crop.loc[dict(grid = coor)] = pct_crop.loc[dict(grid = coor)] - correction
      pct_cft.loc[dict(grid = coor)]  = pct_cft.loc[dict(grid = coor)] * 100 / np.sum(pct_cft.loc[dict(grid = coor)].values)

  suma = pct_lake_sub.values   + pct_wetland_sub.values + \
         pct_urban_sub[0].values + pct_urban_sub[1].values  + pct_urban_sub[2].values  + \
         pct_glacier_sub.values  + \
         pct_natveg_sub.values   + pct_crop_sub.values

  if ( abs(suma - 100) > 2.0*sys.float_info.epsilon ):
    pct_crop.loc[dict(grid = coor)]    = pct_crop.loc[dict(grid = coor)]     * 100/suma
    pct_natveg.loc[dict(grid = coor)]  = pct_natveg.loc[dict(grid = coor)]   * 100/suma
    pct_wetland.loc[dict(grid = coor)] = pct_wetland.loc[dict(grid = coor)]  * 100/suma
    pct_lake.loc[dict(grid = coor)]    = pct_lake.loc[dict(grid = coor)]     * 100/suma
    pct_glacier.loc[dict(grid = coor)] = pct_glacier.loc[dict(grid = coor)]  * 100/suma
    pct_urban.loc[dict(grid = coor)]   = pct_urban.loc[dict(grid = coor)]    * 100/suma

# Reset multindex
pct_cft     = pct_cft.unstack()
pct_crop    = pct_crop.unstack()
pct_natveg  = pct_natveg.unstack()
pct_wetland = pct_wetland.unstack()
pct_lake    = pct_lake.unstack()
pct_glacier = pct_glacier.unstack()
pct_urban   = pct_urban.unstack()

# Create new surface data netcdf file
ds['PCT_CFT']     = pct_cft
ds['PCT_CROP']    = pct_crop
ds['PCT_NATVEG']  = pct_natveg
ds['PCT_WETLAND'] = pct_wetland
ds['PCT_LAKE']    = pct_lake
ds['PCT_GLACIER'] = pct_glacier
ds['PCT_URBAN']   = pct_urban

# Write new surface dataset
fname_new = 'surfdata_360x720cru_50pfts_simyr1850_c240120.nc'
ds.to_netcdf(fname_new, format='NETCDF3_CLASSIC')
