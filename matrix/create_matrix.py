import os
import json
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

json_folder = "C:\\Users\\Marta\\OneDrive - UAM\\TFG\\BBDD\\merged_json_ja4+ja4s+ja4ts"  
app_fingerprints = {}

#Read fingerprints from .json
for filename in sorted(os.listdir(json_folder)):
    if filename.endswith(".json"):
        app_name = filename.replace("ja4+ja4s+ja4ts.json", "")
        filepath = os.path.join(json_folder, filename)

        with open(filepath, "r") as f:
            huellas = json.load(f).get("huellas", [])
            huellas = [h.strip().lower() for h in huellas]
            app_fingerprints[app_name] = set(huellas)

#Calculate similarity matrix
apps = list(app_fingerprints.keys())
sim_matrix = np.zeros((len(apps), len(apps)))

for i, app_a in enumerate(apps):
    for j, app_b in enumerate(apps):
        if i <= j:
            set_a = app_fingerprints[app_a]
            set_b = app_fingerprints[app_b]
            comunes = len(set_a & set_b)
            union = set_a | set_b
            interseccion = set_a & set_b
            similitud = len(interseccion) / len(union) if union else 0


            sim_matrix[i, j] = similitud
            sim_matrix[j, i] = similitud

# crate dataframe for image
df_similitud = pd.DataFrame(sim_matrix, index=apps, columns=apps)
"""
threshold = 0.1
mask = df_similitud < threshold"""

print("\nMatriz de Similitud entre Aplicaciones Web (JA4+JA4S):\n")
print(df_similitud.round(2))

# Heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(df_similitud, cmap="Blues", linewidths=0.5, cbar=True) #añadir: mask=mask para el threshold
plt.title("Similarity Matrix of JA4 + JA4S + JA4TS Fingerprints", fontsize=14)
plt.xlabel("Application")
plt.ylabel("Application")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
