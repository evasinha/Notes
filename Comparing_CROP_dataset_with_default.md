# Comparison of surface dataset and LUT used for CROP vs. default BGC simulation

## Creation of land use timeseries for CROP simulation
1. Created by combining 17 pft LUT `landuse.timeseries_360x720cru_hist_simyr1850-2015_c180220.nc` and NCAR's 78 pfts LUT `landuse.timeseries_360x720cru_hist_78pfts_simyr1850-2015_c170428.nc`.
2. `PCT_CROP` and `PCT_NAT_PFT` were updated based on NCAR LUT.
3. `PCT_CFT` and `FERTNITRO_CFT` were created based on NCAR LUT.
4. [Steps used for creating the CROP land use timeseries](Creating_landuse_timeseries_50pft.md)

## Surface dataset creation for BGC crop simulation with GSWP3 forcing:
* `surfdata_360x720cru_50pfts_simyr1850_c230114.nc`:
	* Created using mksurdata tool
	* 1850 values updated using landuse timeseries (`landuse.timeseries_360x720cru_hist_50pfts_simyr1850-2015_c220216.nc`)
* `surfdata_360x720cru_50pfts_simyr1850_c230518.nc`
	* Few negative `PCT_NATVEG` in the surface dataset listed in above step were causing the cbalance error. These were resolved in this dataset 
* `surfdata_360x720cru_50pfts_simyr1850_c230615.nc`
	* Added values of `APATITE_P` , `LABILE_P` , `OCCLUDED_P` , `SECONDARY_P`.
	* These values were copied from `surfdata_0.5x0.5_simyr1850_c211019.nc` 

	
## Surface dataset creation for BGC crop simulation with WCv2 forcing:
* `surfdata_0.5x0.5_50pfts_simyr1850_c230808.nc`
	* All dimensions and variables copied from `surfdata_0.5x0.5_simyr1850_c211019.nc` except those containing containing cft, natpft, and lsmpft. 
	* These were copied from rotated `surfdata_360x720cru_50pfts_simyr1850_c230615.nc`.

	
## Comparison of CROP surface dataset with default dataset
1. [Comparing percentage cropland area](figures/fig_PCT_CROP.png)
2. [Comparing percentage natural vegeation land unit](figures/fig_PCT_NATVEG.png)
3. [Comparing percentage pf PFT=0 on natural vegetation landunit](figures/fig_PCT_NAT_PFT_0.png)
4. [Comparing percentage pf PFT=1 on natural vegetation landunit](figures/fig_PCT_NAT_PFT_1.png)
5. [Comparing percentage pf PFT=2 on natural vegetation landunit](figures/fig_PCT_NAT_PFT_2.png)
6. [Comparing percentage pf PFT=3 on natural vegetation landunit](figures/fig_PCT_NAT_PFT_3.png)
7. [Comparing percentage pf PFT=4 on natural vegetation landunit](figures/fig_PCT_NAT_PFT_4.png)
8. [Comparing percentage pf PFT=5 on natural vegetation landunit](figures/fig_PCT_NAT_PFT_5.png)
9. [Comparing percentage pf PFT=6 on natural vegetation landunit](figures/fig_PCT_NAT_PFT_6.png)
10. [Comparing percentage pf PFT=7 on natural vegetation landunit](figures/fig_PCT_NAT_PFT_7.png)
11. [Comparing percentage pf PFT=8 on natural vegetation landunit](figures/fig_PCT_NAT_PFT_8.png)
12. [Comparing percentage pf PFT=9 on natural vegetation landunit](figures/fig_PCT_NAT_PFT_9.png)
13. [Comparing percentage pf PFT=10 on natural vegetation landunit](figures/fig_PCT_NAT_PFT_10.png)
14. [Comparing percentage pf PFT=11 on natural vegetation landunit](figures/fig_PCT_NAT_PFT_11.png)
15. [Comparing percentage pf PFT=12 on natural vegetation landunit](figures/fig_PCT_NAT_PFT_12.png)
16. [Comparing percentage pf PFT=13 on natural vegetation landunit](figures/fig_PCT_NAT_PFT_13.png)
17. [Comparing percentage pf PFT=14 on natural vegetation landunit](figures/fig_PCT_NAT_PFT_14.png)

## Comparison of CROP LUT with default LUT
18. [Time series comparing total cropland area](figures/lu_ts_cropland_area.png)