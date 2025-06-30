import os 
import pandas as pd

def save_to_csv(extracted_data, file_name):
    df = pd.DataFrame([extracted_data])
    if not os.path.exists(file_name):
        df.to_csv(file_name, index=False)
    else:
        df.to_csv(file_name, mode='a', index=False, header=False) 
