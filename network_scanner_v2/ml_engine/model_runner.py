import joblib
model1 = joblib.load("./models/iso_forest_model.pkl")
model2 = joblib.load("./models/kmeans_model.pkl")
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.feature_extracter import load_flow_stats_as_dataframe, load_csv_as_dataframe

def test_iso_models():
    X = load_flow_stats_as_dataframe("../core/logs/flow_stats.json")
    # X = X.drop(columns=["timestamp", 'app_protocol', "suspicious_keywords"], errors="ignore")
    X = X.drop(columns=["flow_id"], errors="ignore")
    print("[+] Testing Isolation Forest model...")
    predictions = model1.predict(X)
    print("[+] Isolation Forest model predictions:")
    for i in predictions :
        print(f"Predictions : {1 if i == -1 else -1}")

def test_kmeans_models():
    X = load_csv_as_dataframe("../logs/data_log.csv")
    X = X.drop(columns=["ip_src", "ip_dest", "timestamp", "protocol", "app_protocol", "suspicious_keywords", "error"], errors="ignore")
    print("[+] Testing KMeans model...")
    predictions = model2.predict(X)
    print("[+] KMeans model predictions:")
    print(predictions)

def regressor_model():
    model = joblib.load("./models/regressor_model.pkl")
    metrics = load_csv_as_dataframe("../logs/data_log.csv")

    # Drop unwanted metadata columns
    X = metrics.drop(columns=[
        "ip_src", "ip_dest", "timestamp", "protocol",
        "app_protocol", "suspicious_keywords", "error"
    ], errors="ignore")

    print("[+] Testing Regressor model...")
    predictions = model.predict(X)

    print("[+] Regressor model predictions:\n")
    for i, (has_kw, is_ascii) in enumerate(predictions):
        status = "🚨 Suspicious" if has_kw >= 0.5 else "✅ Clean"
        ascii_flag = "🧾 ASCII" if is_ascii >= 0.5 else "📦 Binary/Encoded"
        print(f"[{i+1:03}] → {status} | Content: {ascii_flag}")

if __name__ == "__main__":
    # test_iso_models()
    # test_kmeans_models()
    regressor_model()
    