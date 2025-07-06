# 🧠 Passive ML Network Scanner (v2)

A modular and efficient passive network scanner powered by scikit-learn models for anomaly detection, clustering, and regression. Integrated with a RESTful FastAPI backend for easy testing and real-time monitoring.

---

## 🚀 Features

- ✅ Real-time traffic log monitoring
- 📊 Supports multiple ML models:
  - Isolation Forest (Anomaly Detection)
  - KMeans Clustering
  - Regression (e.g., CPU/Bandwidth prediction)
- 🧩 Modular structure with easy model swapping
- 📡 Passive mode — no active probing
- 🖥️ FastAPI endpoints for testing and feedback
- 📝 JSON logging of predictions
- 📂 Auto-loads latest CSV logs for prediction

---

## 📁 Project Structure

network_scanner_v2/
|--main.py
|--train_models.py
|--core/
    |-- logs/
    |--device_fingerprinter.py
    |--dns_resolver.py
    |--feartures_extracter.py
    |--packet_sniffer.py
    |--port_scanner.py
    |--traffic_monitor.py
|--logs/
|--ml_engine/
    |--models\
        |--iso_forest_model.pkl
        |--kmeans_model.pkl
        |--regressor_model.pkl
    |--model_runner.py
|--utils\
    |--data_logger.py
    |--log_prediction.py


---

## 🔧 Setup & Installation

```bash
# Clone the repo
git clone <repo_url>
cd network_scanner_v2

# Set up virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```
# Run the Server :
```bash 
uv run main.py
# or if you don't have the uv then 
python main.py
```

# API Endpoints 
| Endpoint                | Method | Description                                 |
| ----------------------- | ------ | ------------------------------------------- |
| `/`                     | GET    | Status & route listing                      |
| `/test_iso`             | GET    | Test Isolation Forest on latest traffic log |
| `/test_kmeans`          | GET    | Test KMeans Clustering                      |
| `/test_regressor`       | GET    | Run regression model on latest metrics      |
| `/latest_csv`           | GET    | Show latest detected CSV files              |
| `/scan`                 | GET    | Trigger new scan & log generation           |
| `/retrain`              | POST   | Retrain models using latest logs            |

# Isolation Forest Model Output:-
```bash 
{
  "status": "✅ ISO Forest model tested",
  "total_predictions": 500,
  "summary": {
    "-1 (anomalies)": 12,
    "1 (normal)": 488,
}
```
--- 

# KMeans Model Output :-
```bash 
{
  "status": "✅ KMeans model tested",
  "total_predictions": 500,
  "clusters": [0, 1, 2]
}
```

---

# Regressor Model output :- 
```bash 
{
  "status": "✅ Regressor model tested",
  "total_predictions": 500,
  "sample": [0.52, 0.61, 0.44, 0.49, 0.71]
}
```
---

# Credit :- 
Built by Moksh Malde with the conquerors spirit and passion ,
Open to the Contribution and Suggestion and more Collaboration with anyone

---
# Status :-
Passive Scanner done ✅
Wait for some updates regarding this project's next part



# Final Words :-
`Nothing is hard until you try it out and give it your best`
-Moksh Malde