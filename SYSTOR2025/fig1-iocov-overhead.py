#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np

import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

# plt.rcParams["font.family"] = "Times New Roman"
# Global font settings
plt.rcParams.update({'font.size': 12, 'font.family': 'Times New Roman'})

output_fig_file = 'fig-iocov-trace-overhead.pdf'

dpi_val = 600

# Usage: python3 fig1-iocov-overhead.py

# Sample data
items = ['ext4', 'XFS', 'Btrfs']
x = np.arange(len(items))
width = 0.35

# Values for left subplot
xfstests_without_iocov = [7032, 7749, 10454]
xfstests_with_iocov = [7677, 8357, 11854]

# Values for right subplot
metis_without_iocov = [230.9, 25.4, 25.2]
metis_with_iocov = [226.1, 24.0, 24.3]

fig, axs = plt.subplots(1, 2, figsize=(8, 4))

# Use color + hatching
colors = ['#1f77b4', '#ff7f0e']  # Blue and Orange (matplotlib defaults)
hatches = ['...', '///']  # Dot-style and slant hatch

# Left subplot
bars_l1 = axs[0].bar(x - width/2, xfstests_without_iocov, width, color=colors[0], edgecolor='black', hatch=hatches[0], label='Without IOCov')
bars_l2 = axs[0].bar(x + width/2, xfstests_with_iocov, width, color=colors[1], edgecolor='black', hatch=hatches[1], label='With IOCov')
# axs[0].set_title('Left Plot')
axs[0].set_xticks(x)
axs[0].set_xticklabels(items)
axs[0].set_ylabel('Completion Time (s)', fontweight='bold', fontsize=12)
# axs[0].set_xlabel('File System', fontweight='bold', fontsize=12)
# axs[0].legend(loc='upper left', fontsize=10, frameon=False)
axs[0].grid(axis='y', linestyle='-', alpha=0.3)

# axs[0].bar_label(bars_l1, padding=3)
# axs[0].bar_label(bars_l2, padding=3)


# Right subplot
bars_r1 = axs[1].bar(x - width/2, metis_without_iocov, width, color=colors[0], edgecolor='black', hatch=hatches[0])
bars_r2 = axs[1].bar(x + width/2, metis_with_iocov, width, color=colors[1], edgecolor='black', hatch=hatches[1])
# axs[1].set_title('Right Plot')
axs[1].set_xticks(x)
axs[1].set_xticklabels(items)
axs[1].set_ylabel('Operations per second', fontweight='bold', fontsize=12)
# axs[1].set_xlabel('File System', fontweight='bold', fontsize=12)
axs[1].grid(axis='y', linestyle='-', alpha=0.3)

# axs[1].bar_label(bars_r1, padding=3)
# axs[1].bar_label(bars_r2, padding=3)

# Remove individual legends:
# axs[0].legend(frameon=False)
# axs[1].legend(frameon=False)

# Create a single legend for both subplots
handles, labels = axs[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=2, frameon=False, bbox_to_anchor=(0.5, -0.05))

# Adjust layout and save
plt.tight_layout()
plt.savefig(output_fig_file, format='pdf', dpi=dpi_val, bbox_inches='tight')
