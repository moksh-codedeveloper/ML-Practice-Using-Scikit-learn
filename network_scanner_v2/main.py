from importlib import reload
from fastapi import FastAPI
from ml_engine.model_runner import test_iso_models, test_kmeans_models, regressor_model
from core.feature_extracter import load_csv_as_dataframe
from ml_engine.model_runner import get_latest_monitor_csv
import uvicorn
import os

app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "🧠 Passive ML Network Scanner API is running!",
        "routes": ["/test_iso", "/test_kmeans", "/test_regressor", "/latest_csv"]
    }

@app.get("/test_iso")
def run_iso():
    predictions = test_iso_models()
    return {
        "status": "✅ ISO Forest model tested",
        "total_predictions": len(predictions),
        "summary": {
            "-1 (anomalies)": int((predictions == -1).sum()),
            "1 (normal)": int((predictions == 1).sum())
        }
    }

@app.get("/test_kmeans")
def run_kmeans():
    predictions = test_kmeans_models()
    return {
        "status": "✅ KMeans model tested",
        "total_predictions": len(predictions),
        "clusters": list(set(predictions))
    }

@app.get("/test_regressor")
def run_regressor():
    predictions = regressor_model()
    return {
        "status": "✅ Regressor model tested",
        "total_predictions": len(predictions),
        "sample": predictions[:5].tolist()
    }

@app.get("/latest_csv")
def latest_csvs():
    try:
        traffic_csv = get_latest_monitor_csv()
        data_csv = get_latest_monitor_csv("../logs/", "data_log")
        return {
            "status": "✅ Latest CSV paths loaded",
            "traffic_monitor_csv": traffic_csv,
            "data_log_csv": data_csv
        }
    except Exception as e:
        return {"error": str(e)}


if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=5000, reload=True)
