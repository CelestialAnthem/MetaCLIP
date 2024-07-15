import json

# 读取第一个JSON文件
with open('metadata_evalset_0704.json', 'r') as f1:
    data1 = json.load(f1)

# 读取第二个JSON文件
with open('metadata.json', 'r') as f2:
    data2 = json.load(f2)

# 获取list并合并
combined_list = data1 + data2

print("Length of first list:", len(data1))
print("Length of second list:", len(data2))

# 查找重复项
unique_set = set()
duplicates = set()

for item in combined_list:
    if item in unique_set:
        duplicates.add(item)
    else:
        unique_set.add(item)

# 剔除重复项后的列表
unique_list = list(unique_set)

print("Length of combined list without duplicates:", len(unique_list))

# 输出结果
with open('metadata_mix_0704_2.json', 'w') as f_out:
    json.dump(unique_list, f_out)

# 如果需要将重复项输出到文件
with open('duplicates.json', 'w') as f_dup:
    json.dump(list(duplicates), f_dup)

print("合并后的JSON文件内容已保存到 metadata_mix_0704.json")
print("重复项已保存到 duplicates.json")
