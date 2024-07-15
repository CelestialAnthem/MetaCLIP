import json
import jsonlines
import logging
from tqdm import tqdm
import concurrent.futures

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def process_item(item):
    images = item["images"]
    text = item["texts"][0][1]
    return {
        "images": images,
        "text": f"<__dj__image> {text} "
    }

def main(dir, dataname):
    logging.info("Starting to read the JSON file")
    # Read the JSON file
    with open('%s/%s.json' % (dir, dataname), 'r', encoding='utf-8') as f:
        data = json.load(f)
    logging.info("JSON file reading completed")

    # Process data with multithreading and show progress bar
    logging.info("Starting to process data")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(tqdm(executor.map(process_item, data), total=len(data), desc="Processing Data"))

    logging.info("Data processing completed")

    # Convert and write to JSONL file
    logging.info("Starting to write the JSONL file")
    with jsonlines.open('%s/%s.jsonl' % (dir, dataname), mode='w') as writer:
        writer.write_all(results)
    logging.info("JSONL file writing completed")

    print("Conversion completed, JSONL file has been generated.")

if __name__ == "__main__":
    main(dir="/share3/LIV/datacomp/processed_data/syh/snorkel_base_0710", dataname="clipensnorkel_0615_metadata_t100000")
