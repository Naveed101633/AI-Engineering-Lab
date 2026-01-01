import sys
import os
import random
# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.db.database import get_connection, save_evaluation
from src.ai.refiner import translate_with_context

def run_batch_test(num_samples=10):
    conn = get_connection()
    cur = conn.cursor()
    
    print(f"🎲 Picking {num_samples} random samples from the knowledge base...")
    cur.execute("SELECT english FROM dictionary ORDER BY RANDOM() LIMIT %s", (num_samples,))
    samples = cur.fetchall()
    cur.close()
    conn.close()

    print(f"🚀 Starting Batch Translation...")
    
    for (eng_text,) in samples:
        print(f"📝 Translating: {eng_text}")
        
        # Get the AI translation using our RAG logic
        translated = translate_with_context(eng_text, "english", "sindhi")
        
        # Save to our evaluation table in Docker
        save_evaluation(
            input_text=eng_text,
            rule_out="N/A (Sentence Mode)", 
            refined_out=translated,
            s_lang="english",
            t_lang="sindhi"
        )
        print(f"✅ Saved: {translated}")

    print(f"\n✨ Evaluation Complete! Results are stored in the 'evaluation_results' table.")

if __name__ == "__main__":
    run_batch_test(10) # Start with 10 to be safe with API tokens