import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42


plt.rcParams["font.family"] = "Times New Roman"


# Data
filesystems = ['RefFS', 'Ext4', 'Ext2', 'XFS', 'BtrFS']
opsPerSecond = [830.0, 280.3, 281.6, 29.2, 29.9]
statesPerSecond = [349.9, 112.6, 173.8, 8.8, 21.2]

# X-axis positions for the bars
x = range(len(filesystems))

# Create the figure and axis objects
fig, ax = plt.subplots()

# Width of the bars
bar_width = 0.4

bar1Color='#2547b8'
bar2Color='#e37d30'


bars1 = ax.bar(x, opsPerSecond, color=bar1Color, width=bar_width, edgecolor='black', linewidth=0.5, hatch='//', label='ops / sec')

bars2 = ax.bar([i + bar_width for i in x], statesPerSecond, color=bar2Color, width=bar_width, edgecolor='black', linewidth=0.5, label='states / sec')

# Set the x-axis labels
ax.set_xticks([i + bar_width / 2 for i in x])
ax.set_xticklabels(filesystems)

# Set the y-axis tick values and labels
yticks = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900]  # Adjust the values as needed
ax.set_yticks(yticks)
ax.set_yticklabels(yticks)

#Write values above bar charts

for i, v in enumerate(opsPerSecond):
    ax.text(i, v + 10, str(v), color=bar1Color, ha='center', va='bottom', fontsize=8)

for i, v in enumerate(statesPerSecond):
    ax.text(i + bar_width, v + 10, str(v), color=bar2Color, ha='center', va='bottom', fontsize=8)


ax.set_axisbelow(True)
#ax.grid(axis='y', linestyle='-', alpha=0.3)

# Add labels and a legend
ax.set_xlabel('File Systems (Using RAM Disks)', fontsize=10)
ax.set_ylabel('Number of Operations Or Unique States', fontsize=10)
#ax.set_title('Number of Operations or Unique States by File System')
ax.legend()

# Save the figure as a PDF
fig.savefig('filesystems-operations-states.pdf', format='pdf', bbox_inches='tight')