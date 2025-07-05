# traffic_monitor.py
from scapy.all import sniff
from collections import defaultdict
import threading
import time
import os 
from scapy.layers.inet import IP, TCP, UDP, ICMP
import csv
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
    log_path = f"logs/traffic_monitor_{time.strftime('%Y%m%d_%H%M%S')}.csv"
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    # Flatten the stats for CSV writing
    rows = []
    for flow, stats in data.items():
        row = {
            "flow_id": flow,
            "total_packets": stats["total_packets"],
            "avg_packet_size": stats["avg_packet_size"],
            "packet_rate": stats["packet_rate"],
            "flow_duration": stats["flow_duration"],
            "protocol": stats["protocol"]
        }
        rows.append(row)

    file_exists = os.path.isfile(log_path)
    with open(log_path, "a", newline="") as csvfile:
        fieldnames = ["flow", "total_packets", "avg_packet_size", "packet_rate", "flow_duration", "protocol"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists or os.stat(log_path).st_size == 0:
            writer.writeheader()
        writer.writerows(rows)

def start_monitoring():
    threading.Thread(target=compute_flow_stats, daemon=True).start()
    sniff(prn=packet_handler, store=False)

if __name__ == "__main__":
    start_monitoring()
