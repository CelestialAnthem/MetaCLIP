import matplotlib.pyplot as plt
import numpy as np
import json

# Load the JSON file
with open("/mnt/share_disk/LIV/datacomp/metaclip/entry_counts.json", 'r') as f:
    data = json.load(f)

# Convert the data to a numpy array
word_counts = np.array(list(data.values()))


# Calculate the number of zeros and values greater than 200
num_zeros = np.sum(word_counts == 0)
num_greater_than_200 = np.sum(word_counts > 200)

# Print the results
print(num_zeros, num_greater_than_200)


plt.xlim(0, 100) 
plt.figure(figsize=(10, 6))
plt.hist(word_counts[word_counts > 0], bins=100, edgecolor='black')
plt.title('Histogram of Values')
plt.xlabel('Value')
plt.ylabel('Frequency')
# plt.xlim(0, 100000) 
plt.xscale('log') 
plt.savefig("./haha.png")