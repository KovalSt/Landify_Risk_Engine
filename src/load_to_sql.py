import pandas as pd
from sqlalchemy import create_engine
import time
import subprocess
import os
# --- CONFIGURATION ---
# Replace 'your_password' with your actual PostgreSQL password in DBeaver.
DB_USER = 'postgres'
DB_PASS = os.getenv('PG_PASSWORD')
if not DB_PASS:
    raise ValueError("Database password not found! Please set the PG_PASSWORD environment variable.")
def get_wsl_host_ip():
    cmd = "ip route show | grep default | awk '{print $3}'"
    return subprocess.check_output(cmd, shell=True).decode('utf-8').strip()

DB_HOST = get_wsl_host_ip()
print(f"Connecting to Windows Host at: {DB_HOST}")
DB_PORT = '5432'
DB_NAME = 'lendify_risk'

DB_URI = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_engine(DB_URI)

def load_csv_to_sql(csv_path, table_name):
    print(f"Starting load for {table_name} from {csv_path}...")
    start_time = time.time()
    chunksize = 50000 
    
    # Initialize a variable to keep an exact count of processed rows
    total_rows_inserted = 0 
    
    try:
        # Removing low_memory=False is actually better here to save RAM during chunking
        for i, chunk in enumerate(pd.read_csv(csv_path, chunksize=chunksize)):
            
            chunk.columns = [col.lower().replace(' ', '_') for col in chunk.columns]
            
            if i == 0:
                chunk.to_sql(table_name, engine, if_exists='replace', index=False)
            else:
                chunk.to_sql(table_name, engine, if_exists='append', index=False)
            
            # Calculate the exact size of the current chunk and add it to our running total
            current_chunk_size = len(chunk)
            total_rows_inserted += current_chunk_size
            
            print(f"  -> Inserted chunk {i+1} ({current_chunk_size} rows) | Total so far: {total_rows_inserted}")
            
        end_time = time.time()
        print(f"✅ Successfully loaded {total_rows_inserted} rows into {table_name} in {round(end_time - start_time, 2)} seconds.\n")
        
    except Exception as e:
        print(f"❌ Error loading {table_name}: {e}")

if __name__ == "__main__":
    # Pointing to the raw data files in your project structure
    app_train_path = 'data/raw/application_train.csv'
    bureau_path = 'data/raw/bureau.csv'
    
    # Run the ETL process
    load_csv_to_sql(app_train_path, 'application_train')
    load_csv_to_sql(bureau_path, 'bureau')