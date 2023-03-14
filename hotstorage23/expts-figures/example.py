import matplotlib.pyplot as plt
import numpy as np

# create some data
categories_all = np.array(['A', 'B', 'C', 'D', 'E'])
values_all = np.array([10, 24, 36, 45, 21])

categories_subset = np.array(['A', 'C', 'E'])
values_subset = np.array([12, 28, 18])

# create a bar plot for the larger set
plt.bar(categories_all, values_all, color='blue', alpha=0.5)

# create a bar plot for the smaller set
plt.bar(categories_subset, values_subset, color='red')

# set the x and y axis labels
plt.xlabel('Categories')
plt.ylabel('Values')

# set the plot title
plt.title('Bar Plot with Subset Highlighted')


# Show the plot
plt.savefig('example.pdf', format='pdf', bbox_inches='tight')
