from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import numpy as np
import joblib 
import os
import sys
import json
from datetime import datetime, timezone
sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # Adjust path to import data_collector
from data_collector import data_collector
from sklearn.linear_model import LinearRegression
# Model path
base_dir = os.path.dirname(os.path.dirname(__file__))
model_path = os.path.join(base_dir, 'models', 'isolation_forest_model.pkl')
model_path_reg = os.path.join(base_dir, 'models', 'linear_regression_model.pkl')
LOG_DIR = os.path.join(base_dir, 'logs')
# Load or define model
if os.path.exists(model_path) and os.path.isfile(model_path_reg):
    print("[+] Loading trained model...")
    model = joblib.load(model_path)
    reg_model = joblib.load(model_path_reg)
else:
    print("[!] Trained model not found. Using default pipeline (not trained).")
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("isolation_forest", IsolationForest(contamination=0.1, random_state=42))
    ])
    model_reg = Pipeline([
        ("scaler", StandardScaler()),
        ("linear_regression", LinearRegression())
    ])
# Convert the collected metrics to a 2D array for training

def prepare_data(metrics):
    features = [
        metrics["process_count"],
        metrics["cpu_percent"],
        metrics["memory_percent"],
        metrics["swap_percent"],
        metrics["disk_percent"],
        metrics["load_avg_1"],
        metrics["load_avg_5"],
        metrics["load_avg_15"],
        metrics["zombie_count"] # Timestamp is not used for training, but can be included if needed
    ]
    return np.array(features).reshape(1, -1)

def iso_model_training(n_samples=400):
    all_data = []
    for _ in range(n_samples):
        metrics = data_collector.collect_metrics()
        data = prepare_data(metrics)
        all_data.append(data)
    X = np.vstack(all_data)
    
    # Train the Isolation Forest model
    model.fit(X)
    
    # Save the trained model
    os.makedirs(os.path.dirname(model_path), exist_ok=True)  # Ensure the directory exists
    joblib.dump(model, model_path)
    
    print(f"Isolation Forest model trained and saved as {model_path}")

def regressor_training(n_samples=600):
    all_X = []
    all_y = []
    for _ in range(n_samples):
        metrics = data_collector.collect_metrics()
        X = prepare_data(metrics)

        # Target: predict multiple continuous values
        y = [
            metrics["cpu_percent"],
            metrics["memory_percent"],
            metrics["swap_percent"],
            metrics["disk_percent"],
            metrics["load_avg_1"],
            metrics["load_avg_5"],
            metrics["load_avg_15"]
        ]

        all_X.append(X)
        all_y.append(y)

    # Features: all except CPU, Target: CPU %
    X = np.vstack(all_X)
    y = np.array(all_y)
    model_reg = Pipeline([
        ("scaler", StandardScaler()),
        ("linear_regression", LinearRegression())
    ])
    model_reg.fit(X, y)
    joblib.dump(model_reg, model_path_reg)
    print(f"[✓] Linear Regression model saved to: {model_path_reg}")

# JSON logger
def log_event(model_name, status, model_path, work_done):
    log_data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model": model_name,
        "status": status,
        "path": model_path,
        "work_done": work_done
    }
    log_file = os.path.join(LOG_DIR, f"{model_name}_log_{datetime.now(timezone.utc).isoformat()}.json")
    with open(log_file, "a") as f:
        f.write(json.dumps(log_data) + "\n")

if __name__ == "__main__":
    iso_model_training()
    regressor_training()
    print("[+] You can now use the trained model for predictions.")