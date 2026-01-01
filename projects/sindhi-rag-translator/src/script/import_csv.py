import pandas as pd
import sys
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Path to our project root (so we can find .env and the CSV)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Load environment variables from .env
load_dotenv()

def import_data():
    csv_file = r'C:\Users\PMYLS\Desktop\sindhi-transliteration-pipeline\data\english-sindhi2.csv'
    if not os.path.exists(csv_file):
        print(f"❌ Error: {csv_file} not found in the root directory!")
        return

    print("⏳ Reading CSV (104k+ rows, please wait)...")
    try:
        df = pd.read_csv(csv_file)
        
        # Ensure column names match our database table
        df.columns = ['english', 'sindhi']

        # Database connection string for SQLAlchemy
        db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        
        # Create the engine
        engine = create_engine(db_url)

        print(f"🚀 Uploading {len(df)} rows to Docker PostgreSQL...")
        
        # This uploads the entire CSV at once
        df.to_sql('dictionary', engine, if_exists='replace', index=False)
        
        print("✅ Data Ingestion Complete!")

    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    import_data()