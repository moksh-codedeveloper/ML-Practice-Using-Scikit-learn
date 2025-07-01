import os 
import json 
import numpy as np 

def extract_features_from_json(json_file):
    features = []
    if not os.path.exists(json_file):
        print("JSON file not found.")
    with open(json_file, 'r') as f:
        try:
          logs = json.load(f)
        except json.JSONDecodeError as e:
          print('An exception occurred')
          return []
    for snapshots in logs:
        for flow_id, flow_stats in snapshots.items():
            vec = [
                flow_stats.get("total_packets", 0),
                flow_stats.get("avg_packet_size", 0.0),
                flow_stats.get("flow_duration", 0.0),
                flow_stats.get("packet_rate", 0.0)
            ]
            features.append(vec)
    return np.array(features)

