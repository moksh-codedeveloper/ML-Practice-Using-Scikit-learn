import joblib
# model1 = joblib.load("./models/iso_forest_model.pkl")
model2 = joblib.load("./models/kmeans_model.pkl")
import os, sys, time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.feature_extracter import load_csv_as_dataframe

def test_iso_models(model_name=joblib.load("./models/iso_forest_model.pkl")):
    X = load_csv_as_dataframe(f"../core/logs/traffic_monitor_{time.strftime('%Y%m%d_%H%M%S')}.csv")
    X = X.drop(columns=["flow_id", "protocol"], errors="ignore")
    predictions = model_name.predict(X)
    return predictions

def test_kmeans_models(model_name=joblib.load("./models/kmeans_model.pkl")):
    X = load_csv_as_dataframe("../logs/data_log.csv")
    X = X.drop(columns=["ip_src", "ip_dest", "timestamp", "protocol", "app_protocol", "suspicious_keywords", "error"], errors="ignore")
    predictions = model_name.predict(X)
    return predictions

def regressor_model(model_name=joblib.load("./models/regressor_model.pkl")):
    metrics = load_csv_as_dataframe("../logs/data_log.csv")
    # Drop unwanted metadata columns
    X = metrics.drop(columns=[
        "ip_src", "ip_dest", "timestamp", "protocol",
        "app_protocol", "suspicious_keywords", "error"
    ], errors="ignore")
    predictions = model_name.predict(X)
    return predictions

test_iso_models()