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

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
import numpy as np

plt.rcParams["font.family"] = "Times New Roman"

dpi_val = 600

output_fig_file = 'metis-swarm-perf.pdf'


ops_csv_file = 'Metis-Swarm-Operations.csv'
states_csv_file = 'Metis-Swarm-Unique-Abstract-States.csv'

df_ops = pd.read_csv(ops_csv_file)
df_states = pd.read_csv(states_csv_file)

ops_hours = df_ops.iloc[:, 1]
states_hours = df_states.iloc[:, 1]

# print('ops_hours: ', ops_hours)
# print('type(ops_hours): ', type(ops_hours))

ops_total = df_ops.iloc[:, 2] / 1000000
states_total = df_states.iloc[:, 2] / 1000000
# sgdp03
ops_node1 = df_ops.iloc[:, 3] / 1000000
states_node1 = df_states.iloc[:, 3] / 1000000
# sgdp04
ops_node2 = df_ops.iloc[:, 4] / 1000000
states_node2 = df_states.iloc[:, 4] / 1000000
# sgdp06
ops_node3 = df_ops.iloc[:, 5] / 1000000
states_node3 = df_states.iloc[:, 5] / 1000000

fig, axs = plt.subplots(1, 2, figsize=(10, 4))

# First subplot
axs[0].plot(ops_hours, ops_total, '-bo', label='Overall (18 VTs)')
axs[0].plot(ops_hours, ops_node1, '--rs', label='Node 1')
axs[0].plot(ops_hours, ops_node2, '-.g^', label='Node 2')
axs[0].plot(ops_hours, ops_node3, ':kP', label='Node 3')
axs[0].set_xlabel('Duration (Hours)', fontweight='bold', fontsize=20)
axs[0].set_ylabel('# of Ops (M)', fontweight='bold', fontsize=20)
# axs[0].set_title('Subplot 1: 2nd Column vs. 3rd Column')
axs[0].grid(axis='y', linestyle='-', alpha=0.3)

# Second subplot
axs[1].plot(states_hours, states_total, '-bo')
axs[1].plot(states_hours, states_node1, '--rs')
axs[1].plot(states_hours, states_node2, '-.g^')
axs[1].plot(states_hours, states_node3, ':kP')
axs[1].set_xlabel('Duration (Hours)', fontweight='bold', fontsize=20)
axs[1].set_ylabel('# of States (M)', fontweight='bold', fontsize=20)
# axs[1].set_title('Subplot 2: 2nd Column vs. 4th Column')
axs[1].grid(axis='y', linestyle='-', alpha=0.3)

axs[0].tick_params(axis='both', labelsize=20)
axs[1].tick_params(axis='both', labelsize=20)

# Get the legend handles and labels from the first subplot
handles, labels = axs[0].get_legend_handles_labels()

# Create a single legend for the entire figure using handles and labels from the first subplot
# fig.legend(handles, labels, loc='upper center')
fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 1.09), ncol=4, fontsize=20, frameon=False)

titles = ['(a) File System Operations', '(b) Unique Abstract States']

for ax, title in zip(axs, titles):
    ax.text(0.5, -0.35, title, transform=ax.transAxes, ha='center', va='center', fontsize=22)

# Tight layout
plt.tight_layout()

# Save the figure as a PDF with 600 dpi
plt.savefig(output_fig_file, dpi=dpi_val, format='pdf', bbox_inches='tight')
