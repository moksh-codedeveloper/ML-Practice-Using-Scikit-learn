from data_collector import scanner
import joblib
import pandas as pd
from scapy.all import sniff
from data_collector import extract_to_csv
import warnings
warnings.filterwarnings("ignore")

# Load models
clf_knn = joblib.load("./models/clf_knn.pkl")
clf_rf = joblib.load("./models/clf_rf.pkl")
clf_svc = joblib.load("./models/clf_svc.pkl")
iso_forest = joblib.load("./models/iso_forest.pkl")
label_encoder = joblib.load("./models/label_encoder_protocol.pkl")
min_max = joblib.load("./models/minmax_scaler.pkl")
one_class = joblib.load("./models/one_class_svm.pkl")
reg_lr = joblib.load("./models/reg_lr.pkl")
reg_rf = joblib.load("./models/reg_rf.pkl")

def extract_data(metrics):
    try:
        # Drop unused fields (non-numeric or not used during training)
        drop_cols = ["timestamps", "src_ip", "dst_ip", "src_mac", "dst_mac", "label"]
        for col in drop_cols:
            metrics.pop(col, None)

        # Ensure all expected keys exist with fallback values
        default_keys = [
            "src_port", "dst_port", "protocol", "packet_size",
            "cpu_percent", "memory_percent", "bytes_sent",
            "bytes_recv", "packet_rate"
        ]
        for key in default_keys:
            if metrics.get(key) is None:
                metrics[key] = 0

        # Encode 'protocol'
        metrics["protocol"] = label_encoder.transform([metrics["protocol"]])[0]

        # Prepare DataFrame for scaling
        df = pd.DataFrame([metrics])

        # Scale features
        features_scaled = min_max.transform(df)

        # Predict using models
        classification = clf_rf.predict(features_scaled)[0]
        predicted_size = reg_rf.predict(features_scaled)[0]
        is_anomaly = iso_forest.predict(features_scaled)[0]

        # Optional: confidence score
        confidence = clf_rf.predict_proba(features_scaled)[0]
        confidence_score = confidence[clf_rf.classes_.tolist().index(classification)]
         # ✅ Log prediction
        log_entry = {
            "class": classification,
            "predicted_size": round(predicted_size, 2),
            "is_anomaly": "Yes" if is_anomaly == -1 else "No",
            "confidence": round(confidence_score, 2)
        }
        extract_to_csv.save_to_csv(log_entry, "live_predictions.csv")

    except Exception as e:
        print("❌ Exception during prediction:", e)

# Start sniffing
print("[🔥] Live packet prediction started. Press CTRL+C to stop.")
sniff(prn=lambda pkt: extract_data(scanner.extract_packet_features(pkt)), store=False)
