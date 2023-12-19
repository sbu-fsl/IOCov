import pickle
import sys
import csv

# open a file, where you stored the pickled data
file1 = open(sys.argv[1], 'rb')
file2 = open(sys.argv[2], 'rb')
# dump information to that file
data1= pickle.load(file1)
data2 = pickle.load(file2)
# close the file
file1.close()
file2.close()

syscalls = []
for item in data1:
    syscalls.append(item)

#print(syscalls)
list = [['syscall','mcfs','lttng']]
for call in syscalls:
    for item in data1[call]:
        count1 = 0
        for sub_item in data1[call][item]:
            count1 += int(data1[call][item][sub_item])

        count2 = 0
        for sub_item in data2[call][item]:
            count2 += int(data2[call][item][sub_item])
        list.append([call+'-'+item,count1,count2])

print(list)
with open('out.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(list)

