import pandas as pd
from google.cloud import bigquery
import os
import pandas_gbq
# 1. Point to the "Passport" we just moved
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcp-key.json"

# 2. Setup your Cloud Destination
project_id = "landify-risk-project"
dataset_id = "credit_data"

def upload_to_bq(csv_path, table_name):
    print(f"🚀 Starting Cloud Upload for {table_name}...")
    
    # Read the data
    df = pd.read_csv(csv_path, low_memory=False)
    
    # Clean column names (BigQuery only allows letters, numbers, and underscores)
    df.columns = [col.lower().replace('.', '_').replace(' ', '_') for col in df.columns]
    
    table_id = f"{project_id}.{dataset_id}.{table_name}"
    
    # Send it to the moon (BigQuery)
    # This will automatically create the schema for you!
    try:
        pandas_gbq.to_gbq(df, table_id, project_id=project_id, if_exists='replace')
        print(f"✅ SUCCESS: {table_name} is live in the BigQuery Sandbox.")
    except Exception as e:
        print(f"❌ ERROR: Could not upload {table_name}: {e}")

if __name__ == "__main__":
    # Uploading the main training data and the bureau data
    upload_to_bq('data/raw/application_train.csv', 'application_train')
    upload_to_bq('data/raw/bureau.csv', 'bureau')