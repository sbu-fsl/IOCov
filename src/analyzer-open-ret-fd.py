#!/usr/bin/env python3

#
# Copyright (c) 2020-2024 Yifei Liu
# Copyright (c) 2020-2024 Erez Zadok
# Copyright (c) 2020-2024 Stony Brook University
# Copyright (c) 2020-2024 The Research Foundation of SUNY
#
# You can redistribute it and/or modify it under the terms of the Apache License, 
# Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0).
#

import pickle
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

# Plot
plot_dpi = 600

output_cov = {}
# Only analyze returned open fd >= 0
with open('output_cov_chdir.pkl', 'rb') as f:
    output_cov = pickle.load(f)

open_rets = output_cov['open']

ret_list = []

for ret, cnt in open_rets.items():
    if ret > 0: # do we consider 0?
        ret_list += [ret] * cnt 

ret_list = pd.Series(ret_list)

# histogram on linear scale
plt.subplot(211)
hist, bins, _ = plt.hist(ret_list, bins=8)

# histogram on log scale. 
# Use non-equal bin sizes, such that they look equal on log scale.
logbins = np.logspace(np.log10(bins[0]),np.log10(bins[-1]),len(bins))
plt.subplot(212)
plt.hist(ret_list, bins=logbins)
plt.xscale('log')

plt.savefig('./Assets/Analysis-Figures/open-ret-fds.pdf', bbox_inches='tight',dpi=plot_dpi)
plt.close('all')
