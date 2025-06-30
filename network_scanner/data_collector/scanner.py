from scapy.all import *
from scapy.layers.inet import TCP, UDP, ICMP, IP
import time , datetime, psutil
from . import extract_to_csv
packet_couter = 0 
packet_timestamps = []
INTERFACE = 'wlan0'
def get_protocol(pkt):
    if pkt.haslayer(TCP):
        return "TCP"
    elif pkt.haslayer(UDP):
        return "UDP"
    elif pkt.haslayer(ICMP):
        return "ICMP"
    else:
        return "OTHER"
    
def extract_packet_features(pkt):
    global packet_counter, packet_timestamps

    # Core Packet Info with safe defaults
    src_ip = pkt[IP].src if pkt.haslayer(IP) else "0.0.0.0"
    dst_ip = pkt[IP].dst if pkt.haslayer(IP) else "0.0.0.0"
    src_mac = getattr(pkt, "src", "00:00:00:00:00:00")
    dst_mac = getattr(pkt, "dst", "00:00:00:00:00:00")
    src_port = pkt.sport if pkt.haslayer(TCP) or pkt.haslayer(UDP) else 0
    dst_port = pkt.dport if pkt.haslayer(TCP) or pkt.haslayer(UDP) else 0
    protocol = get_protocol(pkt) if callable(get_protocol) else "OTHER"
    packet_size = len(pkt)
    timestamps = datetime.datetime.now().isoformat()

    # System Stats
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    net_io = psutil.net_io_counters()
    bytes_sent = net_io.bytes_sent
    bytes_recv = net_io.bytes_recv

    # Packet Rate (1-second window)
    now = time.time()
    packet_timestamps.append(now)
    packet_timestamps = [t for t in packet_timestamps if now - t <= 1]
    pps = len(packet_timestamps)

    # Labeling Logic
    label = "normal" if cpu_usage > 40 or pps < 3 else "anomaly"

    packet_data = {
        "timestamps": timestamps,
        "src_ip": src_ip,
        "dst_ip": dst_ip,
        "src_port": src_port,
        "dst_port": dst_port,
        "src_mac": src_mac,
        "dst_mac": dst_mac,
        "protocol": protocol,
        "packet_size": packet_size,
        "cpu_percent": cpu_usage,
        "memory_percent": memory_usage,
        "bytes_sent": bytes_sent,
        "bytes_recv": bytes_recv,
        "packet_rate": pps,
        "label": label
    }

    # print(f"[📡] Packet Captured: {packet_data}")

    # Save to CSV
    extract_to_csv.save_to_csv(packet_data, "dataset.csv")

    return packet_data  # ⬅️ Now usable in real-time prediction

def packet_handler(pkt):
    try:
        extract_packet_features(pkt)
    except Exception as e:
        print(f"❌ Error parsing packet: {e}")

def start_sniffing():
    print(f"🔍 Sniffing started on interface {INTERFACE}")
    sniff(iface=INTERFACE, prn=packet_handler, store=0)

if __name__ == "__main__":
    start_sniffing()