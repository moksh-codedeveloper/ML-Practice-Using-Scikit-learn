import json
import pandas as pd

import json
import pandas as pd

def load_flow_stats_as_dataframe(json_file):
    rows = []
    with open(json_file, 'r') as f:
        data = json.load(f)  # Load the entire JSON array at once

    for snapshot in data:
        for flow_id, stats in snapshot.items():
            row = {
                "flow_id": flow_id,
                "total_packets": stats["total_packets"],
                "avg_packet_size": stats["avg_packet_size"],
                "packet_rate": stats["packet_rate"],
                "flow_duration": stats["flow_duration"]
            }
            rows.append(row)

    return pd.DataFrame(rows)

def load_csv_as_dataframe(csv_path):
    try:
        df = pd.read_csv(csv_path)
        return df
    except Exception as e:
        print(f"[!] Failed to load CSV: {e}")
        return pd.DataFrame()

def convert_flow_stats_json_to_csv(json_path, csv_path):
    rows = []

    with open(json_path, 'r') as f:
        data = json.load(f)  # entire list of flow snapshots

    for snapshot in data:
        for flow_id, stats in snapshot.items():
            row = stats.copy()
            row["flow_id"] = flow_id
            rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv(csv_path, index=False)
    print(f"[+] Converted '{json_path}' → '{csv_path}' with {len(df)} flows")

# Usage
convert_flow_stats_json_to_csv("./logs/flow_stats.json", "./logs/traffic_monitor.csv")
