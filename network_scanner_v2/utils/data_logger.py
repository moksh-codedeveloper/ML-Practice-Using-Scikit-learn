import os, time
import csv
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
CSV_LOG = os.path.join(LOG_DIR, f"data_log_{time.strftime('%Y%m%d_%H%M%S')}.csv")

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
    return obj

def flatten_log_entry(data, timestamp):
    # Ports data
    ports = data.get("ports", {})
    ip_src = data.get("ip_src", ports.get("ip_src", "0.0.0.0"))
    ip_dest = data.get("ip_dest", ports.get("ip_dest", "0.0.0.0"))
    src_port = data.get("src_port", ports.get("src_port", 0))
    dest_port = data.get("dest_port", ports.get("dest_port", 0))
    protocol = data.get("protocol", ports.get("protocol", ""))

    # Fingerprint
    fingerprint = data.get("fingerprint_preview", {}) or {}
    suspicious = fingerprint.get("suspicious_keywords", [])
    if not isinstance(suspicious, list):
        suspicious = ["none"]
    if not suspicious:
        suspicious = ["none"]
    has_suspicious = 0 if suspicious == ["none"] else 1

    # Flatten CSV
    flat_data = {
        "timestamp": timestamp,
        "ip_src": str(ip_src),
        "ip_dest": str(ip_dest),
        "src_port": int(src_port),
        "dest_port": int(dest_port),
        "protocol": str(protocol),
        "payload_len": int(fingerprint.get("payload_length", 0)),
        "app_protocol": str(fingerprint.get("app_protocol", "")),
        "is_ascii": int(fingerprint.get("is_ascii", 0)),
        "suspicious_keywords": ','.join(suspicious),
        "has_suspicious_keywords": has_suspicious,
        "error": str(data.get("error", ""))
    }

    return flat_data

def log_data(data):
    ensure_log_dir()
    timestamp = datetime.now().isoformat()

    if not isinstance(data, dict):
        print("[!] log_data error: data is not a dictionary")
        return

    data = convert_bools_to_int(data)
    # --- CSV Log ---
    try:
        flat_data = flatten_log_entry(data, timestamp)
        write_header = not os.path.exists(CSV_LOG)
        with open(CSV_LOG, 'a', newline='') as cf:
            writer = csv.DictWriter(cf, fieldnames=flat_data.keys())
            if write_header:
                writer.writeheader()
            writer.writerow(flat_data)
    except Exception as e:
        print(f"[!] Failed to write CSV log: {e}")
