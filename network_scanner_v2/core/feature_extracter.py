import json
import pandas as pd

def load_flow_stats_as_dataframe(json_file):
    with open(json_file, 'r') as f:
        logs = json.load(f)

    rows = []
    for snapshot in logs:
        for flow_id, stats in snapshot.items():
            row = stats.copy()
            row["flow_id"] = flow_id
            rows.append(row)

    df = pd.DataFrame(rows)
    return df
