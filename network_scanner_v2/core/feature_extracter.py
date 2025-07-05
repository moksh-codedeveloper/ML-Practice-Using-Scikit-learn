import pandas as pd
def load_csv_as_dataframe(csv_path):
    try:
        df = pd.read_csv(csv_path)
        return df
    except Exception as e:
        print(f"[!] Failed to load CSV: {e}")
        return pd.DataFrame()
