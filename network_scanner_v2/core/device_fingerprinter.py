from scapy.layers.inet import TCP, UDP
from scapy.packet import Raw

SUSPICIOUS_KEYWORDS = [
    "cmd",
    "sh",
    "exe",
    "powershell",
    "curl",
    "wget",
    "root",
    "login",
    "passwd",
    "bin",
    "bash",
    "python",
]


def device_fingerprinting(pkt):
    if pkt.haslayer(TCP):
        sport = pkt[TCP].sport
        dport = pkt[TCP].dport

        if sport == 80 or dport == 80:
            return "HTTP"
        if sport == 443 or dport == 443:
            return "HTTPS"
        if sport == 22 or dport == 22:
            return "SSH"
        if sport == 21 or dport == 21:
            return "FTP"
        if sport == 25 or dport == 25:
            return "SMTP"
    elif pkt.haslayer(UDP):
        sport = pkt[UDP].sport
        dport = pkt[UDP].dport

        if sport == 53 or dport == 53:
            return "DNS"

    return "UNKNOWN"

def extract_payload_features(pkt):
    payload = b""
    if Raw in pkt:
        payload = bytes(pkt[Raw].load)
    
    try:
      decoded = payload.decode("utf-8", errors="ignore")
    except:
        decoded = ""
    preview = decoded[:30] if decoded else ""
    is_ascii = all(32 <= ord(c) <= 126 for c in decoded[:50]) if decoded else False
    keyword_hits = [kw for kw in SUSPICIOUS_KEYWORDS if kw in decoded.lower()]

    return {
        "payload_length": len(payload),
        "payload_preview": preview,
        "is_ascii": is_ascii,
        "suspicious_keywords": keyword_hits
    }

def fingerprint_packet(pkt):
    return {
        "app_protocol": device_fingerprinting(pkt),
        **extract_payload_features(pkt)
    }

