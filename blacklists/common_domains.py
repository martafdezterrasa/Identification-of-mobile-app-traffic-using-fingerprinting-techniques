import os
import json
from collections import defaultdict

#domains from JSONs
def leer_dominios_json(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        return json.load(f)


input_folders = [
    "iphone12_abuela",
    "iphone12_lucía",
    "iphone13_isa",
    "iphone13mini_carol",
    "iphone15_pau",
    "xiaomi_pocoX3_david",
]

# Dict --> count folders with domains
dominios_en_carpetas = defaultdict(int)

for folder in input_folders:
   
    dominios_json_file = os.path.join(folder, "dominios_repetidos_3_o_mas.json")
    if os.path.exists(dominios_json_file):
        dominios = leer_dominios_json(dominios_json_file)
        
        #Count how many devices contain a domain
        for dominio in dominios:
            dominios_en_carpetas[dominio] += 1

# Filter domains which appear in more
dominios_comunes = {dominio: count for dominio, count in dominios_en_carpetas.items() if count > 1}


print("Common domains:")
print(dominios_comunes)
