import os
import json
from collections import defaultdict


def get_domains(json_data):
   
    dominios = []
    for packet in json_data:
        dominio = packet.get("domain", None)
        if dominio:  # make sure domain is not None
            dominios.append(dominio) 
    return dominios

input_folders = [
    "iphone12_abuela",
    "iphone12_lucía",
    "iphone13_isa",
    "iphone13mini_carol",
    "iphone15_pau",
    "xiaomi_pocoX3_david",
]

#JSON file per folder --> domains repeated 3 or more times
for folder in input_folders:
    # Dict to count each domain
    dominios_carpeta = defaultdict(int)

    for file in os.listdir(folder):
        if file.endswith(".json") and "limpio" not in file: 
            file_path = os.path.join(folder, file)
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            dominios = get_domains(data)
            
            # filter domains
            seen = set()
            for dominio in dominios:
                if dominio not in seen:
                    dominios_carpeta[dominio] += 1   #count each time found
                    seen.add(dominio)
    
    # Filter domains which apper 3 or more times in each application
    dominios_filtrados = {dominio: count for dominio, count in dominios_carpeta.items() if count >= 3}
    
    
    #save
    output_file = os.path.join(folder, "dominios_repetidos_3_o_mas.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(dominios_filtrados, f, indent=4, ensure_ascii=False)

    print(f"File saved in: {output_file} with {len(dominios_filtrados)} domains.")
