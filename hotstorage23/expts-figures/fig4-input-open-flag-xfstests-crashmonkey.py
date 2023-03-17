#!/usr/bin/env python3

import statistics
import matplotlib.pyplot as plt
import numpy as np
import os
import pickle
from scipy.stats import gmean
import math

plt.rcParams["font.family"] = "Times New Roman"

# pkl_dir = '/mcfs2/LTTng-xfstests-2022-1211/IOCov/src'
pkl_dir = os.getcwd()

fig4_xfstests_input = {}
fig4_crashmonkey_input = {}
dpi_val = 600

with open(os.path.join(pkl_dir, 'fig4_input_cov_all_xfstests_xattrs.pkl'), 'rb') as f:
    fig4_xfstests_input = pickle.load(f)

with open(os.path.join(pkl_dir, 'fig4_input_cov_crashmonkey.pkl'), 'rb') as f:
    fig4_crashmonkey_input = pickle.load(f)

fig4_xfstests_open_flags = fig4_xfstests_input['open']['flags']
fig4_crashmonkey_open_flags = fig4_crashmonkey_input['open']['flags']

# print('fig4_xfstests_open_flags: ', fig4_xfstests_open_flags)
# print('fig4_crashmonkey_open_flags: ', fig4_crashmonkey_open_flags)

data1_xfstests = []
data2_crashmonkey = []
data3_diff = []

x_labels = []

# It is true for open flags
crashmonkey_subset_xfstests = True 

for open_flag in sorted(fig4_xfstests_open_flags.keys(), reverse=True):
    x_labels.append(open_flag)
    if fig4_xfstests_open_flags[open_flag] < fig4_crashmonkey_open_flags[open_flag]:
        crashmonkey_subset_xfstests = False
    data1_xfstests.append(fig4_xfstests_open_flags[open_flag])
    data2_crashmonkey.append(fig4_crashmonkey_open_flags[open_flag])
    data3_diff.append(fig4_xfstests_open_flags[open_flag] - fig4_crashmonkey_open_flags[open_flag])

data = np.array([data2_crashmonkey, data3_diff])

labels = ['CrashMonkey', 'xfstests']
# Set up the plot
fig, ax = plt.subplots()

ax.set_xscale('log')

# set the tick locations and labels on the x-axis
# xtick_values = [1, 10, 100, 1000, 10000, 100000, 1000000, 10000000]
# xtick_labels = ['1', '10', '100', '1000', '10000', '100000', '1000000', '10000000']

xtick_values = [0.1, 1, 10, 100, 1000, 10000, 100000, 1000000, 10000000]
# xtick_labels = ['0', '1', '2', '3 (1K)', '4', '5', '6 (1M)', '7 (10M)']
xtick_labels = ['0', '1', '10', '100', '1K', '10K', '100K', '1M', '10M']

plt.xticks(xtick_values, xtick_labels)

ax.set_xlim(xmin = 0.1)

# Create the stacked bar chart
# 'green' 'orange'
ax.barh(x_labels, data[0], color='#4daf4a', label='CrashMonkey')
ax.barh(x_labels, data[1], color='#ff7f0e', left=data[0], hatch='////', label='xfstests')


# Add a title and axis labels
# ax.set_title('Stacked Bar Chart')
ax.set_xlabel('Frequency (log scale base 10)', fontweight='bold')
ax.set_ylabel('Open Flags', fontweight='bold')

# Add a legend
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.1), ncol=len(labels))

# Adjust the plot layout
plt.tight_layout()

# Save the plot to a PDF file as a vector plot
plt.savefig('fig4-open-flag-xfstests-crashmonkey.pdf', format='pdf', bbox_inches='tight')


# print('data1_xfstests: ', data1_xfstests)
# print('data2_crashmonkey: ', data2_crashmonkey)

def safe_log(x):
    """
    Calculate the logarithm of a positive number or return 0 for the logarithm of 0.
    """
    if x > 0:
        return math.log2(x)
    else:
        return 0

def min_max_normalize(lst):
    min_val = min(lst)
    max_val = max(lst)
    normalized_lst = [(x - min_val) / (max_val - min_val) for x in lst]
    return normalized_lst

def safe_geometric_mean(numbers):
    product = 1
    for num in numbers:
        if num != 0:
            product *= num
    return pow(product, 1/len(numbers))

data1_xfstests = min_max_normalize(data1_xfstests)
data2_crashmonkey = min_max_normalize(data2_crashmonkey)

# data1_xfstests = [safe_log(x) for x in data1_xfstests]
# data2_crashmonkey = [safe_log(x) for x in data2_crashmonkey]

# xfstests_avg = statistics.mean(data1_xfstests)
# crashmonkey_avg = statistics.mean(data2_crashmonkey)

xfstests_avg = safe_geometric_mean(data1_xfstests)
crashmonkey_avg = safe_geometric_mean(data2_crashmonkey)

xfstests_avg_list = [xfstests_avg] * len(data1_xfstests)
crashmonkey_avg_list = [crashmonkey_avg] * len(data2_crashmonkey)

def rmsd(actual, predicted):
    """
    Calculate the Root Mean Square Deviation (RMSD) between two lists.
    """
    # Check that the two lists have the same length
    if len(actual) != len(predicted):
        raise ValueError("The two lists must have the same length.")

    # Calculate the squared differences between the actual and predicted values
    squared_differences = [(actual[i] - predicted[i]) ** 2 for i in range(len(actual))]

    # Calculate the mean squared difference
    mean_squared_difference = sum(squared_differences) / len(actual)

    # Calculate the RMSD by taking the square root of the mean squared difference
    rmsd = math.sqrt(mean_squared_difference)

    return rmsd


rmsd_xfstests = rmsd(xfstests_avg_list, data1_xfstests)

rmsd_crashmonkey = rmsd(crashmonkey_avg_list, data2_crashmonkey)

print('rmsd_xfstests: ', rmsd_xfstests)
print('rmsd_crashmonkey: ', rmsd_crashmonkey)
