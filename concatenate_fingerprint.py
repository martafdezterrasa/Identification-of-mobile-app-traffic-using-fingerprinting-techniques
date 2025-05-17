import json
import os

import json
import os
"""
Function to find all of the JA4+ fingerprints and concatenate them in groups
"""
def concatenate_json(file_json, output_json):
    if os.stat(file_json).st_size == 0:  # Verifies if file is empty
        print(f"Error: File {file_json} is empty.")
        return
    # open json
    with open(file_json, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        data = [data]

    # process each packet
    for packet in data:
        ja4_values = []
        #check if JA4 exists
        if "JA4" in packet:
            ja4_values.append(packet["JA4"])
        if "JA4S" in packet:
            ja4_values.append(packet["JA4S"])
        if "JA4TS" in packet:
            ja4_values.append(packet["JA4TS"])
        for key in ["JA4X.1", "JA4X.2", "JA4X.3", "JA4X.4"]:
            if key in packet:
                ja4_values.append(packet[key])
        #Concatenate in a string
        packet["JA4_combined"] = "_".join(str(value) for value in ja4_values if value)
    processed_data = { "huellas": [packet["JA4_combined"] for packet in data if "JA4_combined" in packet] }

    with open(output_json, "w", encoding="utf-8") as file:
        json.dump(processed_data, file, indent=4, ensure_ascii=False) 


# List of folders to process
input_folders = [
    "iphone12_mini_alfonso",
]

# Get each file from folders
input_files = []
for folder in input_folders:
    for file in os.listdir(folder):
        if file.endswith(".json") and "ja4+ja4s+ja4ts" not in file and "ja4" not in file and "ja4+ja4s" not in file:
            input_files.append(os.path.join(folder, file))

for file in input_files:
   
    base_name = os.path.splitext(file)[0]
   
    output_json = f"{os.path.basename(base_name)}limpio.json"
    concatenate_json(file, output_json)
