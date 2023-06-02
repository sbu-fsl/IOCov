import json
from sys import flags
import matplotlib.pyplot as plt
import numpy as np

 
# Opening JSON file
with open('syzkaller_cov.json') as json_file:
    data = json.load(json_file)
    data = data['open']['flags']
    names = list(data.keys())
    values = np.log10(list(data.values()))
    # Print the type of data variable
    print(values)
    plt.bar(range(len(data)), values, tick_label=names)
    plt.xticks(rotation=90)
    plt.show()
 
