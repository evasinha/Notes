# Creating surface data file with increased pfts (50)

* Notes by Alan di Vittoria on [creating land surface datasets for E3SM](https://acme-climate.atlassian.net/wiki/spaces/ED/pages/1708589675/Creating+land+surface+datasets+for+E3SM).

### 1. Load relevant modules and configure the environment:
```
module load intel
module load netcdf
module load hdf5
export LIB_NETCDF=$NETCDF_ROOT/lib
export INC_NETCDF=$NETCDF_ROOT/include
export USER_FC=ifort
export USER_CC=icc
export USER_LDFLAGS="-L$NETCDF_ROOT/lib -lnetcdf -lnetcdff "
export USER_LDFLAGS=$USER_LDFLAGS" -L$HDF5_ROOT/lib -lhdf5 -lhdf5_fortran -lhdf5_cpp -lhdf5_hl -lhdf5hl_fortran "
```

### 2. Modifications for increased pfts
* In directory `~/wrk/E3SM_projects/E3SM/components/elm/tools/mksurfdata_map/src/` modify `src/mkpftMod.F90` and `src/mkvarctl.F90`. 
* These edits are already made in branch [evasinha/lnd/make_surf_data_50pfts](https://github.com/E3SM-Project/E3SM/commit/f51eab91296147cfc860d2c0310914098ed6baf7).

```
src/mkpftMod.F90

integer, parameter :: maxpft = 50

                   'cassava                            ', &
                   'irrigated_cassava                  ', &
                   'cotton                             ', &
                   'irrigated_cotton                   ', &
                   'foddergrass                        ', &
                   'irrigated_foddergrass              ', &
                   'oilpalm                            ', &
                   'irrigated_oilpalm                  ', &
                   'other_grains                       ', &
                   'irrigated_other_grains             ', &
                   'rapeseed                           ', &
                   'irrigated_rapeseed                 ', &
                   'rice                               ', &
                   'irrigated_rice                     ', &
                   'root_tubers                        ', &
                   'irrigated_root_tubers              ', &
                   'sugarcane                          ', &
                   'irrigated_sugarcane                ', &
                   'miscanthus                         ', &
                   'irrigated_miscanthus               ', &
                   'switchgrass                        ', &
                   'irrigated_switchgrass              ', &
                   'poplar                             ', &
                   'irrigated_poplar                   ', &
                   'willow                             ', &
                   'irrigated_willow                   '/)
```

```
src/mkvarctl.F90

integer           , public :: numpft         = 50   ! number of plant types
```

### 3.Compile the `mksurfdata` code:
```
cd ~/wrk/E3SM_projects/E3SM/components/elm/tools/clm4_5/mksurfdata_map/src/

gmake clean

gmake
```

### 4.Run the `mksurfdata.pl` script in “debug” mode (`-d`) to generate the namelist. 
* It is important to do this in steps and generate namelist first so that `mksrf_fvegtyp` can be modified to use the surface data with increased pfts.

```
cd ~/wrk/E3SM_projects/E3SM/components/elm/tools/mksurfdata_map
	
./mksurfdata.pl -res 360x720cru \
-years 1850 \
-d \
-dinlc /compyfs/inputdata \
-usr_mapdir /compyfs/inputdata/lnd/clm2/mappingdata/maps/360x720
	
mv namelist namelist_360x720cru_1850
```	
	
### 5. Modify `mksurfdata` namelist entries for `mksrf_fvegtyp` and `mksrf_flai`:
```
mksrf_fvegtyp  = '/qfs/people/sinh210/wrk/user_inputdata/lnd/clm2/surfdata_map/mksrf_newcrop_c200813.nc'
	
mksrf_flai     = '/qfs/people/sinh210/wrk/user_inputdata/lnd/clm2/surfdata_map/mksrf_lai34cft_simyr2000_c200622.nc'
```

### 6. Create the surface dataset:
* `./mksurfdata_map < namelist_360x720cru_2000`

### 7. Copy the surface dataset to the inputdata directory.
	
### 8. Helpful tips
1. Supported model resolutions are those found in the repository input data directory `$DIN_LOC_ROOT/lnd/clm2/mappingdata/maps`
2. If mapping files are missing on compy then copy them from the NCAR folder:

```
cd /compyfs/inputdata/lnd/clm2/mappingdata/maps/360x720/
svn export https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/lnd/clm2/mappingdata/maps/360x720/map_3x3min_MODIS_to_360x720_nomask_aave_da_c120830.nc 
```
3. If svn export does not working on compy then compy from another machine. Ex from NERSC:
	
```
cd /compyfs/inputdata/lnd/clm2/mappingdata/maps/360x720/
sftp esinha@cori.nersc.gov
cd /global/cfs/cdirs/e3sm/inputdata/lnd/clm2/mappingdata/maps/360x720
mget *.nc
```