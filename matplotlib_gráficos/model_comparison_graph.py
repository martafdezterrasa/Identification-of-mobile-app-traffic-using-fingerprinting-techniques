import matplotlib.pyplot as plt
import numpy as np


accuracies = ['Top-1', 'Top-3', 'Top-5']
x = np.arange(len(accuracies))
bar_width = 0.25

# Accuracy per model
xgboost = [39.23, 64.72, 74.90]
random_forest = [39.67, 66.35, 77.18]
dictionary_match = [58.49, 77.96, 88.35]

plt.figure(figsize=(10, 6))

# For each accuracy --> each model
plt.bar(x - bar_width, xgboost, width=bar_width, label='XGBoost', color='#1f77b4')
plt.bar(x, random_forest, width=bar_width, label='Random Forest', color='#2ca02c')
plt.bar(x + bar_width, dictionary_match, width=bar_width, label='Dictionary Match', color='#ff7f0e')


plt.xticks(x, accuracies)
plt.ylabel('Accuracy (%)')
plt.title('Model Comparison by Accuracy Type (JA4+ Grouping Only)')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)


plt.tight_layout()
plt.show()
