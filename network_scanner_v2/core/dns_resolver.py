from scapy.all import DNS, DNSQR
import socket

SUSPICIOUS_DOMAINS = ['onions', 'desi', 'onion']
dns_stats = {
    "queries": [],
    "resolved_ips": [],
    "failures": 0
}


def resolve_dns(domain):
    try:
    #   print(x)
        ip = socket.gethostbyname(domain)
        return ip
    except:
        return None

def extract_dns_queries(pkt):
    if pkt.haslayer(DNS) and pkt.haslayer(DNSQR):
        try:
            qname = pkt[DNSQR].qname.decode('utf-8', errors="ignore").strip('.')
            return qname
        except:
            return None
    return None

def update_dns_stats(pkt):
    qname = extract_dns_queries(pkt)
    if not qname :
        return
    dns_stats['queries'].append(qname)
    
    resolved_ips = resolve_dns(qname)
    if resolved_ips:
        dns_stats["resolved_ips"].append(resolved_ips)
    else:
        dns_stats["failures"] += 1


def build_dns_features():
    """Returns dictionary of ML-ready DNS features"""
    queries = dns_stats["queries"]
    unique_domains = list(set(queries))
    suspicious_domains = [d for d in queries if any(token in d.lower() for token in SUSPICIOUS_DOMAINS)]
    repeated = len(queries) - len(unique_domains)
    avg_qname_length = sum(len(q) for q in queries) / len(queries) if queries else 0
    has_long_domain = any(len(q) > 50 for q in queries)
    tld_suspicious = any(d.endswith((".ru", ".xyz", ".onion")) for d in queries)

    return {
        "dns_query_count": len(queries),
        "unique_domains_count": len(unique_domains),
        "suspicious_domains_count": len(suspicious_domains),
        "failed_dns_count": dns_stats["failures"],
        "avg_qname_length": round(avg_qname_length, 2),
        "has_long_domain_name": has_long_domain,
        "contains_dot_ru_or_xyz": tld_suspicious,
        "resolved_ips_count": len(dns_stats["resolved_ips"]),
        "repeated_queries": repeated
    }

def reset_dns_stats():
    """Reset stats between sessions"""
    dns_stats["queries"] = []
    dns_stats["resolved_ips"] = []
    dns_stats["failures"] = 0