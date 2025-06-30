import os
import json
import csv
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
JSON_LOG = os.path.join(LOG_DIR, "data_log.json")
CSV_LOG = os.path.join(LOG_DIR, "data_log.csv")

def ensure_log_dir():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
def convert_bools_to_int(obj):
    if isinstance(obj, bool):
        return int(obj)
    elif isinstance(obj, dict):
        return {k: convert_bools_to_int(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_bools_to_int(v) for v in obj]
    else:
        return obj
def log_data(data):
    ensure_log_dir()
    timestamp = datetime.now().isoformat()
    data = convert_bools_to_int(data)
    # Prepare suspicious keywords field
    suspicious = data.get("fingerprint_preview", {}).get("suspicious_keywords", [])
    if not suspicious:
        suspicious = ["none"]
    has_suspicious = 0 if suspicious == ["none"] else 1

    # Prepare JSON log
    json_entry = {
        "timestamp": timestamp,
        **data
    }

    with open(JSON_LOG, 'a') as jf:
        jf.write(json.dumps(json_entry) + '\n')

    # Prepare flat CSV log
    flat_data = {
        "timestamp": timestamp,
        "ip_src": data.get("ip_src", ""),
        "ip_dest": data.get("ip_dest", ""),
        "src_port": data.get("src_port", 0),
        "dest_port": data.get("dest_port", 0),
        "protocol": data.get("protocol", ""),
        "payload_len": data.get("fingerprint_preview", {}).get("payload_length", 0),
        "app_protocol": data.get("fingerprint_preview", {}).get("app_protocol", ""),
        "is_ascii": int(data.get("fingerprint_preview", {}).get("is_ascii", False)),
        "suspicious_keywords": ','.join(suspicious),
        "has_suspicious_keywords": has_suspicious,
        "error": data.get("error", "")
    }

    write_header = not os.path.exists(CSV_LOG)
    with open(CSV_LOG, 'a', newline='') as cf:
        writer = csv.DictWriter(cf, fieldnames=flat_data.keys())
        if write_header:
            writer.writeheader()
        writer.writerow(flat_data)
