from fastapi import FastAPI
from ml_engine.model_runner import test_iso_models, test_kmeans_models, regressor_model, get_latest_monitor_csv
import joblib
import uvicorn
import os

app = FastAPI()

# === Model Paths ===
ISO_MODEL_PATH = "./ml_engine/models/iso_forest_model.pkl"
KMEANS_MODEL_PATH = "./ml_engine/models/kmeans_model.pkl"
REGRESSOR_MODEL_PATH = "./ml_engine/models/regressor_model.pkl"

# === Routes ===
@app.get("/")
def root():
    return {
        "message": "🧠 Passive ML Network Scanner API is running!",
        "routes": ["/test_iso", "/test_kmeans", "/test_regressor", "/latest_csv"]
    }

@app.get("/test_iso")
def run_iso():
    try:
        model = joblib.load(ISO_MODEL_PATH)
        predictions = test_iso_models(model)
        return {
            "status": "✅ ISO Forest model tested",
            "total_predictions": len(predictions),
            "summary": {
                "-1 (anomalies)": int((predictions == -1).sum()),
                "1 (normal)": int((predictions == 1).sum())
            }
        }
    except Exception as e:
        return {"error": f"ISO Model Error: {str(e)}"}

@app.get("/test_kmeans")
def run_kmeans():
    try:
        model = joblib.load(KMEANS_MODEL_PATH)
        predictions = test_kmeans_models(model)
        return {
            "status": "✅ KMeans model tested",
            "total_predictions": len(predictions),
            "clusters": list(set(predictions.tolist()))
        }
    except Exception as e:
        return {"error": f"KMeans Model Error: {str(e)}"}

@app.get("/test_regressor")
def run_regressor():
    try:
        model = joblib.load(REGRESSOR_MODEL_PATH)
        predictions = regressor_model(model)
        return {
            "status": "✅ Regressor model tested",
            "total_predictions": len(predictions),
            "sample_predictions": predictions[:5].tolist()
        }
    except Exception as e:
        return {"error": f"Regressor Model Error: {str(e)}"}

@app.get("/latest_csv")
def latest_csvs():
    try:
        traffic_csv = os.path.normpath(get_latest_monitor_csv("./core/logs", "traffic_monitor"))
        data_csv = os.path.normpath(get_latest_monitor_csv("./logs/", "data_log"))
        return {
            "status": "✅ Latest CSV paths loaded",
            "traffic_monitor_csv": traffic_csv,
            "data_log_csv": data_csv
        }
    except Exception as e:
        return {"error": f"CSV Path Error: {str(e)}"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
