from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest 
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.pipeline import Pipeline
import joblib
from sklearn.cluster import KMeans
from core.feature_extracter import load_csv_as_dataframe
from sklearn.ensemble import RandomForestRegressor
def train_iso_forest_model():
    X = load_csv_as_dataframe("./core/logs/traffic_monitor.csv")
    X = X.drop(columns=["flow_id", "timestamp", 'protocol'], errors='ignore')
    model = IsolationForest(contamination=0.3, random_state=42)
    model.fit(X)
    print("[+] Isolation Forest model trained successfully.")
    joblib.dump(model, "./ml_engine/models/iso_forest_model.pkl")
    
def train_kmeans_model():
    X = load_csv_as_dataframe("./logs/data_log.csv")
    model = Pipeline([
        ("scaler", MinMaxScaler()),
        ("kmeans", KMeans(n_clusters=3, random_state=42))
    ])
    X = X.drop(columns=["ip_src", "ip_dest", "timestamp", "protocol", "app_protocol", "suspicious_keywords", "error"], errors='ignore')
    print("[+] Training KMeans model...")
    model.fit(X)
    print("[+] KMeans model trained successfully.")
    joblib.dump(model, "./ml_engine/models/kmeans_model.pkl")

def regressor_model():
    model = Pipeline([
        ("scaler", StandardScaler()),
        ("regressor", RandomForestRegressor(n_estimators=100, random_state=42))
    ])
    metrics = load_csv_as_dataframe("./logs/data_log.csv")
    X = metrics.drop(columns=["ip_src", "ip_dest", "timestamp", "protocol", "app_protocol", "suspicious_keywords", "error"], errors='ignore')
    Y = metrics[["has_suspicious_keywords", "is_ascii"]] 
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)
    print("[+] Regressor model trained successfully.")
    joblib.dump(model, "./ml_engine/models/regressor_model.pkl")

if __name__ == "__main__":
    # train_kmeans_model()
    train_iso_forest_model()
    # regressor_model()