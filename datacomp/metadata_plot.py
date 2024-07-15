import json
import matplotlib.pyplot as plt

# 读取结果文件
with open("results.json", "r") as f:
    results = json.load(f)

# 提取数据
unigram_values = [freq for _, freq in results["unigram_frequency"]]
bigram_values = [freq for _, freq in results["bigram_frequency"]]
pmi_values = [pmi for _, pmi in results["bigram_pmi"]]

# 绘制直方图
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.hist(unigram_values, bins=50, color='blue', alpha=0.7, log=True)
plt.title('Unigram Frequency')
plt.xlabel('Frequency')
plt.ylabel('Count')

plt.subplot(1, 3, 2)
plt.hist(bigram_values, bins=50, color='green', alpha=0.7, log=True)
plt.title('Bigram Frequency')
plt.xlabel('Frequency')
plt.ylabel('Count')

plt.subplot(1, 3, 3)
plt.hist(pmi_values, bins=50, color='red', alpha=0.7)
plt.title('Bigram PMI')
plt.xlabel('PMI')
plt.ylabel('Count')

plt.tight_layout()
plt.savefig("histograms.png")
print("Histograms saved as histograms.png")
