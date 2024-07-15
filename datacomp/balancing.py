import json
import numpy as np
import sys
import logging
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

sys.path.insert(0, "/root/MetaCLIP/metaclip")
from substr_matching import substr_matching
from balancing import balance_sampling

DIR = "/mnt/share_disk/LIV/datacomp/processed_data/snorkel/metaclip_3clip_en_ratio_snorkel_top40_0615"
OUT_DIR = "/share3/LIV/datacomp/processed_data/syh/"
tag = ""

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 加载元数据和条目计数
logging.info("Loading metadata and entry counts...")
with open("/root/MetaCLIP/metadata%s.json" % tag) as f:
    metadata = json.load(f)

with open("%s/entry_counts%s.json" % (DIR, tag)) as f:
    entry_count_json = json.load(f)

count = 0
for entry in metadata:
    if entry not in entry_count_json:
        count += 1
        print(f"Key not found: {entry}")

print(count)

entry_count = np.array([entry_count_json[entry] for entry in metadata], dtype=np.uint64)

# 加载数据
logging.info("Loading data...")
with open("%s/output%s.json" % (DIR, tag)) as f:
    datas = json.load(f)

def process_data(data, entry_prob):
    text = data["texts"][0]
    text[2] = substr_matching(text[1], metadata)
    curation_prob = min(entry_prob[text[2]].sum(), 1.0)
    curated = balance_sampling(text[2], entry_prob)
    logging.debug(f"[curation_prob={curation_prob:.3f}, curated={curated}] {text[1]}")
    if curated:
        return data
    return None

def save_curated_data(curated_data, filename):
    logging.info(f"Saving curated data to {filename}...")
    with open(filename, 'w') as f:
        json.dump(curated_data, f, indent=4)
    logging.info(f"Curated data saved to {filename}")

def process_data_wrapper(args):
    return process_data(*args)

def run_processing(t):
    logging.info(f"Starting data processing for t={t}...")
    entry_count_adjusted = entry_count.copy()
    entry_count_adjusted[entry_count_adjusted < t] = t
    entry_prob = t / entry_count_adjusted

    # 使用ProcessPoolExecutor进行并行处理
    with ProcessPoolExecutor() as executor:
        results = list(tqdm(executor.map(process_data_wrapper, [(data, entry_prob) for data in datas]), total=len(datas), desc=f"Processing data for t={t}"))

    # 过滤掉None值
    curated_data = [result for result in results if result is not None]

    print(len(curated_data))

    # 保存curated数据
    save_curated_data(curated_data, f"{OUT_DIR}/clipensnorkel_0615_metadata_t{t}{tag}.json")

if __name__ == "__main__":
    t_values = [100000, 200000]  # 你可以根据需要调整这个列表
    for t in t_values:
        run_processing(t)
