from scapy.all import *
from scapy.layers.inet import TCP, UDP, ICMP, IP

def get_protocol(pkt):
    if pkt.haslayer(TCP):
        return "TCP"
    elif pkt.haslayer(UDP):
        return "UDP"
    elif pkt.haslayer(ICMP):
        return "ICMP"
    else:
        return "OTHER"

def port_scanner(pkt):
    if not pkt.haslayer(IP):
        return None  # skip non-IP packets

    ip_src = pkt[IP].src
    ip_dest = pkt[IP].dst

    src_port = None
    dest_port = None

    if pkt.haslayer(TCP):
        src_port = pkt[TCP].sport
        dest_port = pkt[TCP].dport
    elif pkt.haslayer(UDP):
        src_port = pkt[UDP].sport
        dest_port = pkt[UDP].dport

    port_scanned_data = {
        "ip_src": ip_src,
        "ip_dest": ip_dest,
        "src_port": src_port,
        "dest_port": dest_port,
        "protocol": get_protocol(pkt)
    }

    return port_scanned_data
