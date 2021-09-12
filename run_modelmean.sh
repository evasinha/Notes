#!/bin/bash

# ------ Options for running rwdailymean -----
export SITE=US-UiB
#export SITE=US-UiA
#export SITE=US-UiC
export CROP=miscanthus
#export CROP=switchgrass
#export CROP=corn
#export QOI=LH
export CASE_PRE=20210422_${CROP}
#export CASE_PRE=20210507_${CROP}_${QOI}
export CASEID=${CASE_PRE}_${SITE}_ICBCLM45CNCROP_trans
export YR_START=1998
export YR_END=2007
export NSAMPLES=2000
export FNAMEPRE=${CASE_PRE}_${SITE}

export PLIST_FILE=/home/ac.eva.sinha/OLMT/parm_list_${CROP}

# ----- Directory paths -----
export BASE_DIR=/home/ac.eva.sinha
export OUT_DIR=${BASE_DIR}/ELM-Bioenergy/timeseries_plots/
export RUN_DIR_PATH=/lcrc/group/acme/ac.eva.sinha/UQ
export RUN_DIR=${RUN_DIR_PATH}/${CASEID}

# ----- Delete directory created earlier -----
rm -rf ${FNAMEPRE}

#------ Run rwmodelmean -----
srun -n 12 python rwmodelmean_mpi_new.py --plist_file ${PLIST_FILE} --rundir ${RUN_DIR} --nsamples ${NSAMPLES} --caseid ${CASEID} --yr_start ${YR_START} --yr_end ${YR_END} --fnamepre ${FNAMEPRE}

mkdir ${FNAMEPRE}/indiv_ens_member
mv ${FNAMEPRE}/*.nc ${FNAMEPRE}/indiv_ens_member/
python agg_ens_data.py --crop ${CROP^} --outdir ${OUT_DIR} --nsamples ${NSAMPLES} --caseid ${CASEID} --fnamepre ${FNAMEPRE}

python write_ytrain.py --datadir ${OUT_DIR} --nsamples ${NSAMPLES} --caseid ${CASEID} --fnamepre ${FNAMEPRE}
