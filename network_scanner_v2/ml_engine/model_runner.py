import joblib
import hashlib
# model1 = joblib.load("./models/iso_forest_model.pkl")
# model2 = joblib.load("./models/kmeans_model.pkl")
import os, sys, time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.feature_extracter import load_csv_as_dataframe
from utils.log_prediction import log_prediction
# 🔁 Auto-grab the most recent CSV from logs
def get_latest_monitor_csv(log_dir="./core/logs/", file_name="traffic_monitor"):
    csv_files = [f for f in os.listdir(log_dir) if f.startswith(f"{file_name}_") and f.endswith(".csv")]
    if not csv_files:
        raise FileNotFoundError("No traffic monitor CSV logs found.")
    return os.path.join(log_dir, sorted(csv_files)[-1])


def test_iso_models(model_name=joblib.load("./models/iso_forest_model.pkl")):
    X = load_csv_as_dataframe(get_latest_monitor_csv())
    X = X.drop(columns=["flow_id", "protocol"], errors="ignore")
    predictions = model_name.predict(X)
    log_prediction("Isolation", predictions=predictions)
    return predictions

def test_kmeans_models(model_name=joblib.load("./models/kmeans_model.pkl")):
    X = load_csv_as_dataframe(get_latest_monitor_csv("../logs/", "data_logs"))
    X = X.drop(columns=["ip_src", "ip_dest", "timestamp", "protocol", "app_protocol", "suspicious_keywords", "error"], errors="ignore")
    predictions = model_name.predict(X)
    log_prediction("KMeans", predictions=predictions)
    return predictions

def regressor_model(model_name=joblib.load("./models/regressor_model.pkl")):
    metrics = load_csv_as_dataframe(get_latest_monitor_csv("../logs/", "data_log"))
    # Drop unwanted metadata columns
    X = metrics.drop(columns=[
        "ip_src", "ip_dest", "timestamp", "protocol",
        "app_protocol", "suspicious_keywords", "error"
    ], errors="ignore")
    predictions = model_name.predict(X)
    log_prediction("Regressor", predictions=predictions)
    return predictions

def watch_and_test_iso(interval=30):
    print("[*] Watching logs every", interval, "seconds...")
    last_hash = None

    while True:
        try:
            latest_file = get_latest_monitor_csv()
            with open(latest_file, "rb") as f:
                current_hash = hashlib.md5(f.read()).hexdigest()

            if current_hash != last_hash:
                print("\n[⚡] New traffic log found. Running model...")
                test_iso_models()
                last_hash = current_hash
            else:
                print("[*] No new logs. Waiting...")

        except Exception as e:
            print("[!] Error during watch:", e)
        time.sleep(interval)


def watch_and_test_reg(interval=30):
    print("[*] Watching logs every", interval, "seconds...")
    last_hash = None

    while True:
        try:
            latest_file = get_latest_monitor_csv(",,/logs/", "data_log")
            with open(latest_file, "rb") as f:
                current_hash = hashlib.md5(f.read()).hexdigest()

            if current_hash != last_hash:
                print("\n[⚡] New traffic log found. Running model...")
                regressor_model()
                last_hash = current_hash
            else:
                print("[*] No new logs. Waiting...")

        except Exception as e:
            print("[!] Error during watch:", e)

        time.sleep(interval)

def watch_and_test_kmeans(interval=30):
    print("[*] Watching logs every", interval, "seconds...")
    last_hash = None

    while True:
        try:
            latest_file = get_latest_monitor_csv("../logs/", "data_log")
            with open(latest_file, "rb") as f:
                current_hash = hashlib.md5(f.read()).hexdigest()

            if current_hash != last_hash:
                print("\n[⚡] New traffic log found. Running model...")
                test_kmeans_models()
                last_hash = current_hash
            else:
                print("[*] No new logs. Waiting...")

        except Exception as e:
            print("[!] Error during watch:", e)

        time.sleep(interval)
