import json
import nltk
import os
from collections import Counter
from itertools import chain
import math
import jsonlines
from tqdm import tqdm
import string
from nltk.corpus import stopwords

def build_metadata(jsonl_file_path, output_file_path):
    print("NLTK data path:", nltk.data.find("."))
    
    def load_jsonl(jsonl_file):
        with jsonlines.open(jsonl_file) as reader:
            data = [entry for entry in tqdm(reader, desc="Loading JSONL data")]
        return data

    print("Loading JSONL data from:", jsonl_file_path)
    jsonl_data = load_jsonl(jsonl_file_path)

    # 提取文本数据
    print("Extracting text data...")
    captions = []
    for line in tqdm(jsonl_data, desc="Extracting captions"):
        tmp_str = line["text"].replace("<__dj__image>", "").replace("", "")
        captions.extend([tmp_str])
        
    # 停用词和标点符号
    stop_words = set(stopwords.words())
    punctuations = set(string.punctuation)

    # 分词并去除标点符号和停用词
    print("Tokenizing text data and removing punctuation and stopwords...")
    unigrams = []
    bigrams = []
    for caption in tqdm(captions, desc="Tokenizing"):
        tokens = nltk.word_tokenize(caption.lower())  # 转为小写
        tokens = [token for token in tokens if token not in stop_words and token not in punctuations]
        unigrams.extend(tokens)
        bigrams.extend(nltk.bigrams(tokens))

    # 计算词频
    print("Calculating word frequencies...")
    unigram_freq = Counter(unigrams)
    bigram_freq = Counter(bigrams)

    # 计算PMI
    def compute_pmi(bigram, unigram_freq, bigram_freq, total_tokens):
        word1, word2 = bigram
        p_word1 = unigram_freq[word1] / total_tokens
        p_word2 = unigram_freq[word2] / total_tokens
        p_bigram = bigram_freq[bigram] / total_tokens
        pmi = math.log2(p_bigram / (p_word1 * p_word2))
        return pmi

    print("Calculating PMI scores...")
    total_tokens = sum(unigram_freq.values())
    pmi_scores = {bigram: compute_pmi(bigram, unigram_freq, bigram_freq, total_tokens) for bigram in tqdm(bigram_freq, desc="Calculating PMI")}

    # 排序
    print("Sorting results...")
    sorted_unigrams = sorted(unigram_freq.items(), key=lambda x: x[1], reverse=True)
    sorted_bigrams = sorted(bigram_freq.items(), key=lambda x: x[1], reverse=True)
    sorted_pmi = sorted(pmi_scores.items(), key=lambda x: x[1], reverse=True)

    # 保存结果到JSON文件
    results = {
        "unigram_frequency": sorted_unigrams,
        "bigram_frequency": sorted_bigrams,
        "bigram_pmi": sorted_pmi
    }

    with open(output_file_path, "w") as f:
        json.dump(results, f, indent=4)

    print(f"Results saved to {output_file_path}")

# 示例调用
jsonl_data_path = "/mnt/share_disk/LIV/datacomp/processed_data/snorkel/3clip_en_ratio_snorkel_top40_0615.jsonl"
output_file = "results_snokelbest.json"
build_metadata(jsonl_data_path, output_file)
