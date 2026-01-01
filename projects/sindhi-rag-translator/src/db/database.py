import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def create_phonetic_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonetic_rules (
            id SERIAL PRIMARY KEY,
            letter VARCHAR(10),
            sindhi_mapping VARCHAR(10),
            urdu_mapping VARCHAR(10),
            UNIQUE(letter)
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def get_connection():
    """Returns a connection to the PostgreSQL container."""
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

def create_dictionary_table():
    """Creates the dictionary table for the 100k+ rows."""
    conn = get_connection()
    cur = conn.cursor()
    # Using 'TEXT' because some rows are very long sentences
    cur.execute("""
        CREATE TABLE IF NOT EXISTS dictionary (
            id SERIAL PRIMARY KEY,
            english TEXT NOT NULL,
            sindhi TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_english ON dictionary (english);
    """)
    
    # We also need the evaluation table to save our results
    cur.execute("""
        CREATE TABLE IF NOT EXISTS evaluation_results (
            id SERIAL PRIMARY KEY,
            input_text TEXT NOT NULL,
            rule_output TEXT,
            refined_output TEXT,
            source_lang VARCHAR(20),
            target_lang VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Database Tables (Dictionary & Evaluation) Initialized.")

def save_evaluation(input_text, rule_out, refined_out, s_lang, t_lang):
    """Saves a single transformation result to the database."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO evaluation_results (input_text, rule_output, refined_output, source_lang, target_lang) VALUES (%s, %s, %s, %s, %s)",
        (input_text, rule_out, refined_out, s_lang, t_lang)
    )
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    # Running this file directly will set up all your tables
    create_dictionary_table()