# traffic_monitor.py
from scapy.all import sniff, IP, TCP, UDP, ICMP
from collections import defaultdict
import threading
import time
import json
import os 
flow_data = defaultdict(list)
lock = threading.Lock()

def packet_handler(pkt):
    if IP in pkt:
        proto = "OTHER"
        if TCP in pkt:
            proto = "TCP"
        elif UDP in pkt:
            proto = "UDP"
        elif ICMP in pkt:
            proto = "ICMP"

        flow_key = f"{pkt[IP].src} -> {pkt[IP].dst} | {proto}"
        pkt_info = {
            "timestamp": time.time(),
            "size": len(pkt),
            "protocol": proto
        }

        with lock:
            flow_data[flow_key].append(pkt_info)

def compute_flow_stats():
    while True:
        time.sleep(10)  # Adjust interval as needed

        with lock:
            stats = {}
            for flow, packets in flow_data.items():
                sizes = [p["size"] for p in packets]
                times = [p["timestamp"] for p in packets]

                duration = max(times) - min(times) if len(times) > 1 else 0.001
                stats[flow] = {
                    "total_packets": len(packets),
                    "avg_packet_size": sum(sizes) / len(sizes),
                    "packet_rate": len(packets) / duration,
                    "flow_duration": duration,
                    "protocol": packets[0]["protocol"]
                }

            save_flow_stats(stats)
            flow_data.clear()

def save_flow_stats(data):
    log_path = "logs/flow_stats.json"

    # Ensure logs directory exists
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    if not os.path.exists(log_path):
        with open(log_path, "w") as f:
            json.dump([data], f, indent=2)
    else:
        with open(log_path, "r+") as f:
            try:
                logs = json.load(f)
            except:
                logs = []
            logs.append(data)
            f.seek(0)
            json.dump(logs, f, indent=2)

def start_monitoring():
    threading.Thread(target=compute_flow_stats, daemon=True).start()
    sniff(prn=packet_handler, store=False)

if __name__ == "__main__":
    start_monitoring()
