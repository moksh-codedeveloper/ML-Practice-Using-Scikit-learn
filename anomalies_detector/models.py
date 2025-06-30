import joblib
import time
from data_collector import data_collector

clf = joblib.load("./models/rf_model.pkl")

def extract(metrics):
    return [[
        metrics["process_count"],
        metrics["swap_percent"],
        metrics["memory_percent"],
        metrics["cpu_percent"],
        metrics["disk_percent"],
        metrics["load_avg_1"],
        metrics["load_avg_5"],
        metrics["load_avg_15"],
        metrics["zombie_count"]
    ]]

print("🔍 Starting live anomaly detection...")
while True:
    metrics = data_collector.collect_metrics()
    features = extract(metrics)
    prediction = clf.predict(features)[0]
    
    print(f"[CPU: {metrics['cpu_percent']}%] =>", end=" ")
    if prediction == 1:
        print("⚠️ Anomaly Detected!")
        print(f"""
    🧠 Full Metrics Snapshot:
    ▸ CPU Usage        : {metrics['cpu_percent']}%
    ▸ RAM Usage        : {metrics['memory_percent']}%
    ▸ Swap Usage       : {metrics['swap_percent']}%
    ▸ Disk Usage       : {metrics['disk_percent']}%
    ▸ Load Average 1m  : {metrics['load_avg_1']}
    ▸ Load Average 5m  : {metrics['load_avg_5']}
    ▸ Load Average 15m : {metrics['load_avg_15']}
    ▸ Zombie Processes : {metrics['zombie_count']}
    ▸ Process Count    : {metrics['process_count']}
    """)
    else:
        print("✅ Normal")
    
    time.sleep(2)
