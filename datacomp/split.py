import json
import logging
import os
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor

n = 10
# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 读取JSON文件
file_path = '/mnt/share_disk/LIV/datacomp/metaclip/output.json'
with open(file_path, 'r') as file:
    original_list = json.load(file)
logging.info(f'Loaded JSON file: {file_path}')
logging.info(f'Original list length: {len(original_list)}')

# 将列表平均分成10份
chunk_size = len(original_list) // n
chunks = [original_list[i:i + chunk_size] for i in range(0, len(original_list), chunk_size)]

# 如果列表不能被整除，将剩余的元素分配到最后一块
if len(original_list) % n != 0:
    last_chunk = chunks[-2] + chunks[-1]
    chunks = chunks[:-2] + [last_chunk]

# 打印每个块的长度以进行验证
for i, chunk in enumerate(chunks):
    logging.info(f'Chunk {i+1}: {len(chunk)} items')

# 保存每一块为新的JSON文件的函数
def save_chunk(i, chunk, output_dir):
    output_path = os.path.join(output_dir, f'chunk_{i+1}.json')
    with open(output_path, 'w') as file:
        json.dump(chunk, file)
    logging.info(f'Saved chunk {i+1} to {output_path}')

# 多进程保存
output_dir = '/mnt/share_disk/LIV/datacomp/metaclip/split%d/' % n
os.makedirs(output_dir, exist_ok=True)  # 确保输出目录存在

with ProcessPoolExecutor() as executor:
    # 提交任务到进程池并使用tqdm显示进度
    list(tqdm(executor.map(save_chunk, range(len(chunks)), chunks, [output_dir]*len(chunks)), total=len(chunks), desc='Saving chunks'))
