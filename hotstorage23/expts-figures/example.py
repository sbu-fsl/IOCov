import matplotlib.pyplot as plt
import numpy as np

# Create the data for the horizontal bar chart
y = np.array(['A', 'B', 'C', 'D', 'E'])
x = np.array([10, 15, 20, 25, 30])

# Create the horizontal bar chart
fig, ax = plt.subplots()
ax.barh(y, x)

# Set the arrow
arrow_index = 2
arrow_x = x[arrow_index]
arrow_y = y[arrow_index]
arrow_text = f'Bar {arrow_index+1}'
ax.annotate(arrow_text, xy=(arrow_x, arrow_y), xytext=(arrow_x+5, arrow_y),
             arrowprops=dict(facecolor='red', arrowstyle='->'))

# Add labels and titles
ax.set_xlabel('Value')
ax.set_ylabel('Category')
ax.set_title('Horizontal Bar Chart')

# Save the chart as a vector PDF file
fig.savefig('example.pdf', format='pdf', bbox_inches='tight')
