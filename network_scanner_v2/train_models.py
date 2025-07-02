from sklearn.ensemble import RandomForestClassifier 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest 
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
import joblib
from sklearn.cluster import KMeans
from core.feature_extracter import load_flow_stats_as_dataframe

def train_iso_forest_model():
    X = load_flow_stats_as_dataframe("./core/logs/flow_stats.json")
    X.drop(columns=["flow_id", "timestamp", 'protocol'])
    model = IsolationForest(contamination=0.3, random_state=42)
    model.fit(X)
    print("[+] Isolation Forest model trained successfully.")
    joblib.dump(model, "./ml_engine/models/iso_forest_model.pkl")
    
def train_kmeans_model():
    X = load_flow_stats_as_dataframe("./core/logs/flow_stats.json")
    model = Pipeline([
        ("scaler", MinMaxScaler()),
        ("kmeans", KMeans(n_clusters=3, random_state=42))
    ])
    
    print("[+] Training KMeans model...")
    model.fit(X)
    print("[+] KMeans model trained successfully.")
    joblib.dump(model, "./ml_engine/models/kmeans_model.pkl")

if __name__ == "__main__":
    train_iso_forest_model()
    print("[+] All models trained successfully.")
    print("[+] Models saved to disk.")
    print("[+] You can now use these models for anomaly detection and clustering tasks.")