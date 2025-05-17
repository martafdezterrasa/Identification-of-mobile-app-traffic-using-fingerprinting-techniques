
from collections import defaultdict, Counter
import os
import json
import random

json_folder = "merged_iphone" 
with open("min_counts.json", "r") as f:
    min_counts = json.load(f)


results = {}
seed = 100 #random seed
random.seed(seed)
train_ratio = 0.9 # train ratio of 90%
train_data = {}
test_data = {}


for filename in sorted(os.listdir(json_folder)):
    app_name = filename.replace(".json", "")
    filepath = os.path.join(json_folder, filename)

    with open(filepath, "r") as f:
        fingerprints = json.load(f).get("huellas", [])
        fingerprints = [h.strip().lower() for h in fingerprints]
        random.shuffle(fingerprints)

        # subsampling with the common min
        n = min_counts.get(app_name, 0)
        fingerprints = fingerprints[:n]

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

for app, fingerprints in test_data.items():
    for fingerprint in fingerprints:
        fingerprint = fingerprint.strip().lower()
        y_true.append(app)

        # count apps associated with a fingerprint
        app_counts = Counter(fingerprint_index.get(fingerprint, []))

        if not app_counts:
            y_pred.append("unknown")
            unknown += 1
        else:
            top_apps = [a for a, _ in app_counts.most_common(3)]
            top_5 = [a for a,_ in app_counts.most_common(5)]
            y_pred.append(top_apps[0])  # top-1 prediction

            if app == top_apps[0]:
                correct_top1 += 1
            if app in top_apps:
                correct_top3 += 1
            if app in top_5:
                correct_top5 +=1

total = len(y_true)
accuracy_top1 = (correct_top1 / total) * 100
accuracy_top3 = (correct_top3 / total) * 100
accuracy_top5 = (correct_top5 / total) * 100
unknown_pct = (unknown / total) * 100
incorrectas = total - correct_top1 - unknown
incorrectas_pct = (incorrectas / total) * 100

#Results
print(f"\nEvaluation Results")
print(f"total{total}")
print(f"Top-1 Accuracy: {accuracy_top1:.2f}%")
print(f"Top-3 Accuracy: {accuracy_top3:.2f}%")
print(f"Top-5 Accuracy: {accuracy_top5:.2f}%")
print(f"Unknown: {unknown} ({unknown_pct:.2f}%)")
