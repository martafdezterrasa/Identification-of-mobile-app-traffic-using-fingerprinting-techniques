import os
import json
import numpy as np
import pickle
import time
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import FeatureHasher
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

# folder with json files
input_folders = [
    "C:\\Users\\Marta\\OneDrive - UAM\\TFG\\BBDD\\merged_json_ja4+ja4s+ja4ts"
]

top_3_correct = 0
top_5_correct = 0
total_samples = 0

#get all jsons
input_files = []
for folder in input_folders:
    for file in os.listdir(folder):
        if file.endswith(".json"):
            input_files.append(os.path.join(folder, file))

# Parameters of hashing trick
NUM_FEATURES = 200
hasher = FeatureHasher(n_features=NUM_FEATURES, input_type="string")

x_data = []  # complete vector
y_data = []  # labels
x_data_individual = []  # Individual vectors
y_data_individual = []  # Individual labels

#read each file
for file in input_files:
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    fingerprints = data.get("huellas", [])  

    if not fingerprints:
        print(f"Empty file: {file}")
        continue  #if empty, continue

    # Transform set of fingerprints to a single vector
    x_vector = hasher.transform([{h: 1 for h in fingerprints}]).toarray()[0]
    x_data.append(x_vector)

    # transform each fingerprint to single vectors
    for fingerprint in fingerprints:
        x_individual = hasher.transform([{fingerprint: 1}]).toarray()[0]
        x_data_individual.append(x_individual)
        y_data_individual.append(file)

    # get label from filename
    label = os.path.basename(file).split("_")[-1].replace(".json", "")
    if label.endswith("ja4+ja4s+ja4ts"):
        label = label[:-14]  # remove the last characters not belonging to the app name

    y_data.append(label)

#Transform list to numpy arrays
x_data = np.array(x_data)
y_data = np.array(y_data)
x_data_individual = np.array(x_data_individual)
y_data_individual = np.array(y_data_individual)

# Code labels to be consecutive numbers
encoder = LabelEncoder()
encoder.fit(y_data)
y_data_encoded = encoder.transform(y_data)

encoder_individual = LabelEncoder()
encoder_individual.fit(y_data_individual)
y_data_individual_encoded = encoder_individual.transform(y_data_individual)

# combine both implementations
x_data_combined = np.vstack((x_data, x_data_individual))
y_data_combined = np.concatenate((y_data_encoded, y_data_individual_encoded))

# Cross validation instead of train_test_split
kf = StratifiedKFold(n_splits=15, shuffle=True, random_state=42)

accuracies = []
avg_times_per_fold = []

for train_index, test_index in kf.split(x_data_combined, y_data_combined):
    x_train, x_test = x_data_combined[train_index], x_data_combined[test_index]
    y_train, y_test = y_data_combined[train_index], y_data_combined[test_index]
    
    # Train RandomForest model
    modelRF = RandomForestClassifier(n_estimators=150, random_state=42)
    modelRF.fit(x_train, y_train)
    
    # Evaluate model
    start_time = time.time()
    y_pred = modelRF.predict(x_test)
    prediction_time = time.time() - start_time
    avg_time = prediction_time / len(x_test)
    avg_times_per_fold.append(avg_time)

    #y_pred = modelRF.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)
    accuracies.append(accuracy)
    y_proba = modelRF.predict_proba(x_test)
    for true_label, proba in zip(y_test, y_proba):
        top3 = np.argsort(proba)[::-1][:3]
        top5 = np.argsort(proba)[::-1][:5]
        
        if true_label in top3:
            top_3_correct += 1
        if true_label in top5:
            top_5_correct += 1
        total_samples += 1    
    print(f"Accuracy in each iteration: {accuracy * 100:.2f}%")

print(f"Top-3 accuracy: {top_3_correct / total_samples * 100:.2f}%")
print(f"Top-5 accuracy: {top_5_correct / total_samples * 100:.2f}%")
print(f"Average accuracy: {np.mean(accuracies) * 100:.2f}%")

final_avg_time = sum(avg_times_per_fold) / len(avg_times_per_fold)
print(f"Average time per sample: {final_avg_time:.6f} s")

output_path = "tiempos_modelos.txt"

# Open time file as ("a") to not overwrite and add the time
with open(output_path, "a") as f:
    f.write(f"Random Forest - Average time per sample: {final_avg_time:.6f} seconds\n")

# Save model
with open("randomforest_model.pkl", "wb") as f:
    pickle.dump(modelRF, f)

# Save label encoder 
with open("label_encoder.pkl", "wb") as f:
    pickle.dump(encoder, f)


