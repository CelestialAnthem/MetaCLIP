from build_metadata import build_metadata

id = "3clip_en_ratio_snorkel_top40_0615"
sub_path = "snorkel"
dir = "/mnt/share_disk/LIV/datacomp/processed_data/%s" % sub_path
jsonl_data_path = "/mnt/share_disk/LIV/datacomp/processed_data/%s/%s.jsonl" % (sub_path, id)
output_metadata_path = "/mnt/share_disk/LIV/datacomp/processed_data/%s/metadata_%s.json" % (sub_path, id)

build_metadata(jsonl_data_path,)

