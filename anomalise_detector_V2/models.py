# models.py
import numpy as np
from data_collector import data_collector
from datetime import datetime, timezone
# Prepare the features (must match training structure)
def prepare_data(metrics):
    return np.array([
        metrics["process_count"],
        metrics["cpu_percent"],
        metrics["memory_percent"],
        metrics["swap_percent"],
        metrics["disk_percent"],
        metrics["load_avg_1"],
        metrics["load_avg_5"],
        metrics["load_avg_15"],
        metrics["zombie_count"]
    ]).reshape(1, -1)

def run_models(iso_model, reg_model):
    metrics = data_collector.collect_metrics()

    if "error" in metrics:
        return {
            "status": "error",
            "message": metrics["error"],
            "timestamp": metrics.get("timestamp")
        }

    data = prepare_data(metrics)
    anomaly_flag = int(iso_model.predict(data)[0])

    # Multi-output regression prediction
    predictions = reg_model.predict(data)[0]

    regression_result = {
        "predicted_cpu": float(predictions),
        "predicted_ram": float(predictions),
        "predicted_swap": float(predictions),
        "predicted_disk": float(predictions),
        "predicted_load_1": float(predictions),
        "predicted_load_5": float(predictions),
        "predicted_load_15": float(predictions)
    }

    return {
        "status": "success",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "anomaly": True if anomaly_flag == -1 else False,
        "anomaly_flag": anomaly_flag,
        "regression_prediction": regression_result,
        "source_metrics": metrics
    }
