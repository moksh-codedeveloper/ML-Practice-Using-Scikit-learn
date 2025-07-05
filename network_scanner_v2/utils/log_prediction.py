import os
import csv
import time

CSV_LOG = f"logs/predictions_log{time.strftime('%Y%m%d_%H%M%S')}.csv"
MD_LOG = f"logs/predictions_summary{time.strftime('%Y%m%d_%H%M%S')}.md"

def log_prediction(model_name, predictions):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    os.makedirs("logs", exist_ok=True)

    # --- CSV Logging ---
    write_header = not os.path.exists(CSV_LOG)
    with open(CSV_LOG, "a", newline='') as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["timestamp", "model", "prediction_index", "prediction_value"])

        for i, pred in enumerate(predictions):
            writer.writerow([timestamp, model_name, i, pred])

    # --- Markdown Summary (last N only) ---
    recent = predictions[:10]  # Show only first 10 predictions
    with open(MD_LOG, "w") as f:
        f.write(f"# 🧠 Model Prediction Summary\n")
        f.write(f"**Timestamp:** {timestamp}\n\n")
        f.write(f"**Model:** `{model_name}`\n")
        f.write(f"**Total Predictions:** `{len(predictions)}`\n\n")
        f.write("## 🔍 Sample Predictions (First 10)\n")
        f.write("| Index | Value |\n|-------|--------|\n")
        for i, p in enumerate(recent):
            f.write(f"| {i} | {p} |\n")

    print(f"[+] Logged predictions for {model_name} to CSV and Markdown")
