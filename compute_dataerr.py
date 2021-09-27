#!/usr/bin/env python

import os
import numpy as np
import pickle as pk

from utils import *
from plotutils import *

myrc()

# Load previously generated surrogates and training data
results_all = pk.load(open('results_all.pk', 'rb'))
yall = np.loadtxt('ytrain.dat')
nall, nout = yall.shape #1600, 730

# Load previously generated observational error
dataerr_all = np.loadtxt('dataerr_all_obs.dat').reshape(-1,)

surr_errors = np.zeros(nout,)
for iout in range(nout):
    results = results_all[iout]
    
    if results is not None: 
        if 'rel_l2_val' in results: 
            surr_errors[iout] = results['rel_l2_val'] * np.linalg.norm(yall[:, iout])/np.sqrt(nall)
        else:
            surr_errors[iout] = 0
    else:
        surr_errors[iout] = 0

# Estimate new data error by augmenting surrogate errors to observational errors
dataerr_all_new = np.sqrt(dataerr_all**2 + surr_errors**2)

np.savetxt('dataerr_all.dat', dataerr_all_new)
