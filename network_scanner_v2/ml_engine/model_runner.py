import hashlib
import os, sys, time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.feature_extracter import load_csv_as_dataframe
from utils.log_prediction import log_prediction

# 🔐 Safe & upgraded CSV fetcher
def get_latest_monitor_csv(log_dir="./core/logs/", file_name="traffic_monitor"):
    if not os.path.exists(log_dir):
        raise FileNotFoundError(f"[!] Log directory does not exist: {log_dir}")

    csv_files = [
        f for f in os.listdir(log_dir)
        if f.startswith(f"{file_name}_") and f.endswith(".csv")
    ]
    if not csv_files:
        raise FileNotFoundError(f"[!] No CSV files found with prefix '{file_name}_' in {log_dir}")

    return os.path.join(log_dir, sorted(csv_files)[-1])

# 🔎 ISO Forest
def test_iso_models(model_name):
    X = load_csv_as_dataframe(get_latest_monitor_csv("./core/logs/", "traffic_monitor"))
    X = X.drop(columns=["flow_id", "protocol"], errors="ignore")
    predictions = model_name.predict(X)
    log_prediction("Isolation", predictions=predictions)
    return predictions

# 🔎 KMeans
def test_kmeans_models(model_name):
    X = load_csv_as_dataframe(get_latest_monitor_csv("./logs/", "data_log"))
    X = X.drop(columns=["ip_src", "ip_dest", "timestamp", "protocol", "app_protocol", "suspicious_keywords", "error"], errors="ignore")
    predictions = model_name.predict(X)
    log_prediction("KMeans", predictions=predictions)
    return predictions

# 🔎 Regressor
def regressor_model(model_name):
    metrics = load_csv_as_dataframe(get_latest_monitor_csv("./logs/", "data_log"))
    X = metrics.drop(columns=["ip_src", "ip_dest", "timestamp", "protocol", "app_protocol", "suspicious_keywords", "error"], errors="ignore")
    predictions = model_name.predict(X)
    log_prediction("Regressor", predictions=predictions)
    return predictions

# 👁️ Watchers
def watch_and_test_iso(interval=30):
    print("[*] Watching ISO logs every", interval, "seconds...")
    last_hash = None
    model_path = "./models/iso_forest_model.pkl"

    while True:
        try:
            latest_file = get_latest_monitor_csv("./core/logs/", "traffic_monitor")
            with open(latest_file, "rb") as f:
                current_hash = hashlib.md5(f.read()).hexdigest()

            if current_hash != last_hash:
                print("\n[⚡] New traffic log found. Running ISO model...")
                test_iso_models(model_path)
                last_hash = current_hash
            else:
                print("[*] No new logs. Waiting...")

        except Exception as e:
            print("[!] ISO Watcher Error:", e)

        time.sleep(interval)

def watch_and_test_kmeans(interval=30):
    print("[*] Watching KMeans logs every", interval, "seconds...")
    last_hash = None
    model_path = "./models/kmeans_model.pkl"

    while True:
        try:
            latest_file = get_latest_monitor_csv("./logs/", "data_log")
            with open(latest_file, "rb") as f:
                current_hash = hashlib.md5(f.read()).hexdigest()

            if current_hash != last_hash:
                print("\n[⚡] New traffic log found. Running KMeans model...")
                test_kmeans_models(model_path)
                last_hash = current_hash
            else:
                print("[*] No new logs. Waiting...")

        except Exception as e:
            print("[!] KMeans Watcher Error:", e)

        time.sleep(interval)

def watch_and_test_reg(interval=30):
    print("[*] Watching Regressor logs every", interval, "seconds...")
    last_hash = None
    model_path = "./models/regressor_model.pkl"

    while True:
        try:
            latest_file = get_latest_monitor_csv("./logs/", "data_log")
            with open(latest_file, "rb") as f:
                current_hash = hashlib.md5(f.read()).hexdigest()

            if current_hash != last_hash:
                print("\n[⚡] New traffic log found. Running Regressor model...")
                regressor_model(model_path)
                last_hash = current_hash
            else:
                print("[*] No new logs. Waiting...")

        except Exception as e:
            print("[!] Regressor Watcher Error:", e)

        time.sleep(interval)
