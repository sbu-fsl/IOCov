import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42


plt.rcParams["font.family"] = "Times New Roman"

output_fig_file = 'reffs-perf-log.pdf'

# Data
filesystems = ['RefFS', 'Ext4', 'Ext2', 'XFS', 'BtrFS']
opsPerSecond = [830.0, 280.3, 281.6, 29.2, 29.9]
statesPerSecond = [349.9, 112.6, 173.8, 8.8, 21.2]

# X-axis positions for the bars
x = range(len(filesystems))

# Determine the width and height in inches
width_inches = 5  # Example width for a two-column area
height_inches = 2 # Example height, adjust as needed

# Create the figure and axis objects
# fig, ax = plt.subplots()
fig, ax = plt.subplots(figsize=(width_inches, height_inches))

# Width of the bars
bar_width = 0.4

bar1Color='#1f77b4'
bar2Color='#ff7f0e'

bars1 = ax.bar(x, opsPerSecond, color=bar1Color, width=bar_width, edgecolor='black', linewidth=0.5, hatch='//', label='ops / sec')

bars2 = ax.bar([i + bar_width for i in x], statesPerSecond, color=bar2Color, width=bar_width, edgecolor='black', linewidth=0.5, label='states / sec')

# Set the x-axis labels
ax.set_xticks([i + bar_width / 2 for i in x])
ax.set_xticklabels(filesystems)

# Set the y-axis tick values and labels
# yticks = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900]  # Adjust the values as needed
# yticks = [0, 200, 400, 600, 800, 1000]

ax.set_yscale('log')

ytick_values = [0.1, 1, 10, 100, 1000]
ytick_labels = ['0', '1', '10', '100', '1K']

ax.set_yticks(ytick_values)
ax.set_yticklabels(ytick_labels)

#Write values above bar charts

for i, v in enumerate(opsPerSecond):
    ax.text(i, v + 10, str(v), color=bar1Color, ha='center', va='bottom', fontsize=9)

for i, v in enumerate(statesPerSecond):
    ax.text(i + bar_width, v + 10, str(v), color=bar2Color, ha='center', va='bottom', fontsize=9)


ax.set_axisbelow(True)
#ax.grid(axis='y', linestyle='-', alpha=0.3)

# Add labels and a legend
ax.set_xlabel('File Systems (Using RAM Disks)', fontsize=10, fontweight='bold')
# ax.set_ylabel('Number of Operations Or Unique States', fontsize=10)
ax.set_ylabel('# of Ops or States (log 10)', fontsize=10, fontweight='bold')
#ax.set_title('Number of Operations or Unique States by File System')
ax.legend()

fig.tight_layout()

# Save the figure as a PDF
fig.savefig(output_fig_file, format='pdf', bbox_inches='tight')
