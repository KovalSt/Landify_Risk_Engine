import pandas as pd
from sqlalchemy import create_engine
import time
import subprocess
# --- CONFIGURATION ---
# Replace 'your_password' with your actual PostgreSQL password in DBeaver.
DB_USER = 'postgres'
DB_PASS = '123456789'
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
    
    # We use a 'chunksize' of 50,000 rows to keep memory usage low
    chunksize = 50000 
    
    try:
        # Read the CSV in chunks
        for i, chunk in enumerate(pd.read_csv(csv_path, chunksize=chunksize, low_memory=False)):
            
            # Standardize column names (lowercase, no spaces)
            chunk.columns = [col.lower().replace(' ', '_') for col in chunk.columns]
            
            # 'replace' automatically creates the schema/table on chunk 0
            if i == 0:
                chunk.to_sql(table_name, engine, if_exists='replace', index=False)
            else:
                chunk.to_sql(table_name, engine, if_exists='append', index=False)
            
            print(f"  -> Inserted chunk {i+1} (Rows: {(i+1)*chunksize})")
            
        end_time = time.time()
        print(f"✅ Successfully loaded {table_name} in {round(end_time - start_time, 2)} seconds.\n")
        
    except Exception as e:
        print(f"❌ Error loading {table_name}: {e}")

if __name__ == "__main__":
    # Pointing to the raw data files in your project structure
    app_train_path = 'data/raw/application_train.csv'
    bureau_path = 'data/raw/bureau.csv'
    
    # Run the ETL process
    load_csv_to_sql(app_train_path, 'application_train')
    load_csv_to_sql(bureau_path, 'bureau')