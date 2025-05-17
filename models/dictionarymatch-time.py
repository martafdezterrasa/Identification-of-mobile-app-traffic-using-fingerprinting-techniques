
from collections import defaultdict, Counter
import os
import json
import random
import time

json_folder = "merged_json" 

results = {}
seed = 100 #random seed
random.seed(seed)
train_ratio = 0.9 #train ratio of 90%
train_data = {}
test_data = {}


for filename in sorted(os.listdir(json_folder)):
    app_name = filename.replace("limpio.json", "") #extract app name from filename
    filepath = os.path.join(json_folder, filename)

    with open(filepath, "r") as f:
        fingerprints = json.load(f).get("huellas", [])
        random.shuffle(fingerprints)
        #load fingerprint, shuffle with random seed and divide in train and test
        split_idx = int(len(fingerprints) * train_ratio)
        train_data[app_name] = fingerprints[:split_idx]
        test_data[app_name] = fingerprints[split_idx:]
#inverted index --> each fingerprint has list of apps        
fingerprint_index = defaultdict(list)

for app, fingerprints in train_data.items():
    for fingerprint in fingerprints:
        fingerprint = fingerprint.strip().lower()
        fingerprint_index[fingerprint].append(app)
y_true = [] #true labels
y_pred = [] #predicted labels

correct_top1 = 0
correct_top5 = 0
correct_top3 = 0
unknown = 0

prediction_times = []

for app, fingerprints in test_data.items():
    for fingerprint in fingerprints:
        fingerprint = fingerprint.strip().lower()
        y_true.append(app)

        start = time.time()
        # count apps associated with a fingerprint
        app_counts = Counter(fingerprint_index.get(fingerprint, []))

        if not app_counts:
            y_pred.append("unknown")
            unknown += 1
        else:
            predicted_app = app_counts.most_common(1)[0][0]
        end = time.time()
        prediction_times.append(end - start)

total = len(y_true)
accuracy_top1 = (correct_top1 / total) * 100

unknown_pct = (unknown / total) * 100
incorrectas = total - correct_top1 - unknown
incorrectas_pct = (incorrectas / total) * 100

#Resultados
print(f"\nEvaluation Results")
print(f"total{total}")
print(f"Top-1 Accuracy: {accuracy_top1:.2f}%")

print(f"Unknown: {unknown} ({unknown_pct:.2f}%)")

total_prediction_time = sum(prediction_times)
avg_prediction_time = total_prediction_time / len(prediction_times)
output_path = "tiempos_modelos.txt"

# Open time file as "a" to not overwrite and add the time
with open(output_path, "a") as f:
    f.write(f"Dictionary - Average time per sample: {avg_prediction_time:.6f} segundos\n")
