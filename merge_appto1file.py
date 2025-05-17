import os
import json
from collections import defaultdict


input_folders = [
    "samsungal_a52",
    "xiaomi11_carlota",
    "xiaomi_pocoX3_david"
]

#get the json files according to the group
input_files = []
for folder in input_folders:
    for file in os.listdir(folder):
        if file.endswith("limpio.json") and "ja4+ja4s+ja4ts" not in file and "ja4" not in file and "ja4+ja4s" not in file:
            input_files.append(os.path.join(folder, file))

#dict to group all fingerprints by app
grouped_huellas = defaultdict(list)

#read json files and group by app -- name
for file in input_files:
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
        filename = os.path.basename(file)
        app_name = filename.split("_")[1].replace("limpio.json", "")  # extract app name
        if "huellas" in data:
            grouped_huellas[app_name].extend(data["huellas"])

#Save results -- one file per app
output_folder = "merged_android"
os.makedirs(output_folder, exist_ok=True)

for app_name, huellas in grouped_huellas.items():
    output_file = os.path.join(output_folder, f"{app_name}.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({"huellas": huellas}, f, indent=4, ensure_ascii=False)

print(f"Combined files saved in: {output_folder}")