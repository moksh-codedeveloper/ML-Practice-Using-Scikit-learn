# core/packet_sniffer.py

from scapy.all import sniff
from core.port_scanner import port_scanner, get_protocol
from core.dns_resolver import build_dns_features, update_dns_stats
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import data_logger
from core.device_fingerprinter import fingerprint_packet

def live_sniffer(pkt):
    try:
        ports = port_scanner(pkt)
        protocol = get_protocol(pkt)

        if ports:
            print(f"Source IP: {ports['ip_src']}, Destination IP: {ports['ip_dest']}, "
                  f"Source Port: {ports['src_port']}, Destination Port: {ports['dest_port']}, "
                  f"Protocol: {protocol}")
        else:
            print("Non-IP packet or no ports detected.")

        # DNS features and stats
        update_dns_stats(pkt)
        dns_features = build_dns_features()
        dns_stats = {}  # Set to empty or your real-time DNS stats collector if any

        fingerprint = fingerprint_packet(pkt)
        print(f"[DNS] {dns_features}")
        print(f"[Fingerprint] {fingerprint}")

        log_entry = {
            "ports": ports or {},
            "ip_src": ports['ip_src'] if ports else "0.0.0.0",
            "ip_dest": ports['ip_dest'] if ports else "0.0.0.0",
            "src_port": ports['src_port'] if ports else 0,
            "dest_port": ports['dest_port'] if ports else 0,
            "protocol": protocol,
            "dns_features": dns_features,
            "dns_stats": dns_stats,
            "fingerprint_preview": fingerprint,
            "error": None
        }

        data_logger.log_data(log_entry)

    except Exception as e:
        print(f"[Sniffer Error] {e}")
        data_logger.log_data({"error": str(e)})

def run_sniffer(count, timeout):
    print(f"[⚡] Sniffing {count} packets or until timeout = {timeout}s")
    sniff(filter="ip", prn=live_sniffer, store=False, count=count, timeout=timeout)
    return f"✅ Sniffed {count} packets or until timeout"
