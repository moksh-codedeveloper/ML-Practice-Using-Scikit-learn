# 🧠 Anomalise Detector V2

**Anomalise Detector V2** is a powerful, real-time system monitoring and anomaly detection tool, powered by **scikit-learn**, **FastAPI**, and machine learning. It goes beyond basic logging to actively predict system anomalies and regression-based metrics like CPU load, memory, etc., with modular retraining support.

---

## ⚡ Features

- 🧠 **Unsupervised Anomaly Detection** using Isolation Forest.
- 📈 **Regression-based Prediction** (e.g., CPU usage forecast).
- 🔄 **Live retraining support** via API (`/retrain`).
- 📦 **FastAPI backend** with JSON responses.
- 🗃️ **Historical logs** stored as `.jsonl` files.
- 🧪 Modular, extensible pipeline for adding classifiers or time-series models.
- 📉 Pluggable with **Streamlit/React** dashboards.

---

## 📁 Project Structure
---
    anomalise_detector_V2/
    ├── data_collector/
    │ └── data_collector.py # Collects system metrics
    ├── logs/
    │ └── predictions_log.jsonl # Historical predictions
    ├── models/
    │ ├── isolation_forest_model.pkl
    │ └── linear_regression_model.pkl
    ├── train_models/
    │ └── train_model.py # Model training logic
    ├── main.py # FastAPI server
    ├── models.py # Inference logic
    ├── requirements.txt
    └── README.md
---

## 🚀 Getting Started

### 🧱 Prerequisites

- Python 3.8+
- `pip install -r requirements.txt`

### ▶️ Run the API

```bash
uvicorn main:app --reload
Server runs on http://localhost:8000
```
# 🔍 Endpoints
## GET /predict

Predicts:

Whether the current system snapshot is anomalous

Regression prediction (e.g., CPU percent)

All system metrics returned in response

## 📦 Sample Output:
```json
{
  "status": "success",
  "timestamp": "...",
  "anomaly": true,
  "anomaly_flag": -1,
  "regression_prediction": 62.3,
  "source_metrics": 
  {
    "cpu_percent": 75.5,
    "memory_percent": 68.2,
    ...
  }
}
```
---

## POST /retrain

### Trigger retraining of one of the models.

📥 Request (JSON):
```json
{
  "n_samples": 100,
  "model_name": "isolation_forest"
}
```
📤 Response:
```json
{
    "message": "Isolation Forest model retrained with 100 samples." 
}
```
✅ Accepted model_name: isolation_forest, linear_regression
---
# 🧪 How It Works
## 🧠 Isolation Forest
Learns "normal" behavior from system metrics

Flags outliers as anomalies (-1)

## 📊 Linear Regression
Predicts continuous values (e.g., CPU usage)

Can be extended to predict memory, load average, etc.

## 📉 Historical Logging
Every prediction is logged in logs/predictions_log.jsonl

Can be used for future supervised training
--- 
# 🛠️ Advanced Usage
🎛️ Streamlit Dashboard
```bash
pip install streamlit
streamlit run streamlit_app.py
```
Visualize live predictions and metrics in a browser dashboard.
---
# 🧠 Roadmap
Feature	Status	Notes:-

    🧠 Isolation Forest	✅ Complete	Unsupervised anomaly detection
    📊 Regression Model (CPU)	✅ Complete	Predicts CPU load
    🔁 API-based Retraining	✅ Complete	Supports custom sample counts
    📉 Historical Logging	✅ Complete	.jsonl format
    🧩 Add Classification Model	🔜 Planned	Detect ["normal", "suspicious"]
    ⏱️ Time-Series / LSTM Model	🔜 Planned	Anomaly detection over sequences
    📊 Dashboard (Streamlit/React)	🔜 In progress	Live metric visualizations
---
# 💡 Contribution Ideas
 Add CLI support

 Add Docker support

 Stream anomalies to Telegram/Slack

 Train on labeled log data

# ⚠️ Disclaimer
This tool is intended for educational and research purposes in cybersecurity, system monitoring, and AI automation. Use it responsibly.

# 👨‍💻 Author
# Moksh Malde aka catian scientist 🧪

# Powered by 🐍 Python, 🐱 FastAPI, and Machine Learning
--- 
# 🧠 Philosophy
## "The world can erase my bloodline, but never extinguish the fire — someone will carry this will."