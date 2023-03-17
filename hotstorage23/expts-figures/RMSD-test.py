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
