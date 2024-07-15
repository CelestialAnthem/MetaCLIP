import concurrent.futures
import json
import logging
import os
from tqdm import tqdm

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def count_occurrences_single(file_path, output_path, metadata):
    # Load data from the specific file
    with open(file_path) as f:
        data_json = json.load(f)

    # Initialize local counts
    local_count = {key: 0 for key in metadata}
    for item in data_json:
        for text in item["texts"]:
            for index in text[-1]:
                if index < len(metadata):
                    local_count[metadata[index]] += 1

    # Convert results to JSON
    result_json = json.dumps(local_count, indent=4)
    # Save the results to a corresponding output file
    with open(output_path, "w") as f:
        f.write(result_json)

    # Log completion
    logging.info(f"Results written to {output_path}")
    return output_path

def main():
    tag = "_snorkel"
    directory = "/mnt/share_disk/LIV/datacomp/processed_data/snorkel/metaclip_3clip_en_ratio_snorkel_top40_0615"

    # Load metadata
    with open("/root/MetaCLIP/metadata%s.json" % tag) as f:
        metadata = json.load(f)

    # Prepare to process files in parallel
    logging.info("Starting parallel processing")
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = []
        input_path = os.path.join(directory, "output%s.json" % tag)
        # output_file = f"entry_count_{json_file.split('_')[-1]}"
        output_file = "entry_counts%s.json" % tag
        
        output_path = os.path.join(directory, output_file)
        futures.append(executor.submit(count_occurrences_single, input_path, output_path, metadata))

        # Track progress with tqdm
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(futures), desc="Processing"):
            logging.info(f"Completed processing for {future.result()}")

if __name__ == "__main__":
    main()
