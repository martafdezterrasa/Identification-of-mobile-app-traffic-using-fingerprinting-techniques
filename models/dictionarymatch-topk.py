
from collections import defaultdict, Counter
import os
import json
import random

json_folder = "merged_json" 

results = {}
seed = 100 #random seed
random.seed(seed)
train_ratio = 0.9 #train ratio of 90%
train_data = {}
test_data = {}


for filename in sorted(os.listdir(json_folder)):
    app_name = filename.replace("limpio.json", "") #extract name from filename
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

#creation of confusion matrix
"""import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
import itertools

# Filter out "unkwown" cases
filtered_y_true = []
filtered_y_pred = []
for yt, yp in zip(y_true, y_pred):
    if yp != "unknown":
        yt.replace("limpio", "")
        yp.replace("limpio", "")
        filtered_y_true.append(yt)
        filtered_y_pred.append(yp)

# get ordered apps list
all_apps = sorted(set(filtered_y_true + filtered_y_pred))
for app in all_apps:
    app.replace("limpio", "")
app_to_idx = {app: i for i, app in enumerate(all_apps)}
idx_to_app = {i: app for app, i in app_to_idx.items()}

# Create confusion matrix
y_true_idx = [app_to_idx[app] for app in filtered_y_true]
y_pred_idx = [app_to_idx[app] for app in filtered_y_pred]

conf_matrix = confusion_matrix(y_true_idx, y_pred_idx, labels=range(len(all_apps)))
apps = [app.replace("limpio", "") for app in all_apps]

plt.figure(figsize=(14, 12))
sns.heatmap(conf_matrix, cmap="Blues", 
            xticklabels=apps, 
            yticklabels=apps,
            linewidths=0.5)

plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Real")
plt.xticks(rotation=90)
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()

# confirm accuracy
diagonal_sum = np.trace(conf_matrix)
matrix_total = np.sum(conf_matrix)
accuracy_from_matrix = (diagonal_sum / matrix_total) * 100
print(f"Accuracy from confusion matrix: {accuracy_from_matrix:.2f}%")"""

