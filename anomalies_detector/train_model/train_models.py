from sklearn.ensemble import RandomForestClassifier
import numpy as np 
import joblib 
import sys
import os
import time
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

sys.path.append(os.path.dirname(os.path.dirname(__file__))) 
from data_collector import data_collector

X = []
Y = []

def metrics_extracted(metrics):
    return [
        metrics["process_count"],
        metrics["swap_percent"],
        metrics["memory_percent"],
        metrics["cpu_percent"],
        metrics["disk_percent"],
        metrics["load_avg_1"],
        metrics["load_avg_5"],
        metrics["load_avg_15"],
        metrics["zombie_count"]
    ]

# ✅ Step 1: Collect Normal System Data
print("🚦 Collecting NORMAL system data...")
for _ in range(100):
    metrics = data_collector.collect_metrics()
    X.append(metrics_extracted(metrics))
    Y.append(0)  # normal label
    time.sleep(1)

print("⚠️ Collecting ANOMALOUS system data...")
for _ in range(100):
    metrics = data_collector.collect_metrics()
    X.append(metrics_extracted(metrics))
    Y.append(1)  # anomaly label
    time.sleep(1)

# ✅ Step 3: Train the Model
X_datasets = np.array(X)
Y_label = np.array(Y)
X_train , X_test, Y_train, Y_test = train_test_split(X_datasets, Y_label, test_size=0.2, random_state=42)

clf = RandomForestClassifier(n_estimators=100, random_state=42)
print("🧠 Training your model...")
clf.fit(X_train, Y_train)
print("[+] Training completed :)")

# ✅ Step 4: Save Model
base_dir = os.path.dirname(os.path.dirname(__file__))
model_path = os.path.join(base_dir, "models", "rf_model.pkl")
joblib.dump(clf, model_path)
print("[+] Model saved to:", model_path)

# ✅ Step 5: Evaluate
print("📊 Classification Report:")
print(classification_report(Y_test, clf.predict(X_test)))
