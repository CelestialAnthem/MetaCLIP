import json
from tqdm import tqdm
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 读取结果文件
with open("results.json", "r") as f:
    results = json.load(f)
uni_count = len(results["unigram_frequency"])
bi_count = len(results["bigram_frequency"])
logger.info(f"Number of total unigrams: {uni_count}")
logger.info(f"Number of total bigrams: {bi_count}")
# 提取并筛选数据
filtered_unigrams = [item[0] for item in tqdm(results["unigram_frequency"], desc="Filtering Unigrams") if item[1] > 10]

# 筛选同时满足bigram词频超过10和pmi超过10的bigram
filtered_bigrams = []
bigram_freq_dict = {" ".join(bigram): freq for bigram, freq in results["bigram_frequency"]}
bigram_pmi_dict = {" ".join(bigram): pmi for bigram, pmi in results["bigram_pmi"]}

for bigram_str, freq in tqdm(bigram_freq_dict.items(), desc="Filtering Bigrams"):
    if freq > 5 and bigram_pmi_dict.get(bigram_str, 0) > 15:
        filtered_bigrams.append(bigram_str)

# 合并筛选结果
filtered_results = filtered_unigrams + filtered_bigrams

# 保存筛选结果到新的JSON文件
output_file = "metadata_evalset_0704.json"
with open(output_file, "w") as f:
    json.dump(filtered_results, f)

# 输出筛选结果的数量
logger.info(f"Number of filtered unigrams: {len(filtered_unigrams)}")
logger.info(f"Number of filtered bigrams: {len(filtered_bigrams)}")
logger.info(f"Total filtered items: {len(filtered_results)}")
