import matplotlib.pyplot as plt


models = ['XGBoost', 'Random Forest', 'Dictionary']
times = [0.221, 0.208, 0.028]

# Create graph
plt.figure(figsize=(8, 5))
bars = plt.bar(models, times, color=['orange', 'green', 'steelblue'])

# Labels
plt.title('Average Prediction Time per Sample (JA4+)', fontsize=14)
plt.ylabel('Time (milliseconds)', fontsize=12)
plt.xlabel('Model', fontsize=12)

# Shows values above bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.000002,
             f'{height:.3f}', ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.savefig('prediction_times.pdf', format='pdf')
plt.show()
