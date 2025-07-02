import joblib
model1 = joblib.load("./models/iso_forest_model.pkl")
model2 = joblib.load("./models/kmeans_model.pkl")
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.feature_extracter import load_flow_stats_as_dataframe

def test_iso_models():
    X = load_flow_stats_as_dataframe("../core/logs/flow_stats.json")
    # X = X.drop(columns=["timestamp", 'app_protocol', "suspicious_keywords"], errors="ignore")
    X = X.drop(columns=["flow_id"], errors="ignore")
    print("[+] Testing Isolation Forest model...")
    predictions = model1.predict(X)
    print("[+] Isolation Forest model predictions:")
    print(predictions)

if __name__ == "__main__":
    test_iso_models()