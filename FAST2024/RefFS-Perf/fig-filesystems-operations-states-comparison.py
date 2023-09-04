import matplotlib.pyplot as plt

# Data
filesystems = ['RefFS', 'Ext4', 'Ext2', 'XFS', 'BtrFS']
opsPerSecond = [830.0, 280.3, 281.6, 29.2, 29.9]
statesPerSecond = [349.9, 112.6, 173.8, 8.8, 21.2]

# X-axis positions for the bars
x = range(len(filesystems))

# Create the figure and axis objects
fig, ax = plt.subplots()

# Width of the bars
bar_width = 0.35


bars1 = ax.bar(x, opsPerSecond, width=bar_width, label='ops / sec')

bars2 = ax.bar([i + bar_width for i in x], statesPerSecond, width=bar_width, label='states / sec')

# Set the x-axis labels
ax.set_xticks([i + bar_width / 2 for i in x])
ax.set_xticklabels(filesystems)

# Set the y-axis tick values and labels
yticks = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900]  # Adjust the values as needed
ax.set_yticks(yticks)
ax.set_yticklabels(yticks)

# Add labels and a legend
ax.set_xlabel('File Systems (Using RAM Disks)')
ax.set_ylabel('Number of Operations Or Unique States')
#ax.set_title('Number of Operations or Unique States by File System')
ax.legend()

# Save the figure as a PDF
fig.savefig('filesystems-operations-states.pdf', format='pdf', bbox_inches='tight')