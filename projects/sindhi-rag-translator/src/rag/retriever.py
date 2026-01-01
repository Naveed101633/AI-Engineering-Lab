# src/rag/retriever.py
from src.db.database import get_connection

def retrieve_context(text: str, limit: int = 5):
    """
    Smarter Retrieval: Searches for the full phrase first, 
    then falls back to individual word matching to ensure 
    the Knowledge Base always provides evidence.
    """
    conn = get_connection()
    cur = conn.cursor()
    
    # Clean the text and split into words
    search_phrase = f"%{text.strip()}%"
    words = [f"%{w.strip()}%" for w in text.split() if len(w) > 2] # ignore tiny words like 'is', 'a'

    try:
        # 1. Try to find the exact or partial phrase first (Best Quality)
        query = "SELECT english, sindhi FROM dictionary WHERE english ILIKE %s LIMIT %s"
        cur.execute(query, (search_phrase, limit))
        results = cur.fetchall()

        # 2. If no exact phrase, search for individual words (Fallback)
        if not results and words:
            # Build a dynamic query: WHERE english ILIKE %s OR english ILIKE %s...
            word_conditions = " OR ".join(["english ILIKE %s" for _ in words])
            query = f"SELECT english, sindhi FROM dictionary WHERE {word_conditions} LIMIT {limit}"
            cur.execute(query, tuple(words))
            results = cur.fetchall()

        return results 
    except Exception as e:
        print(f"🔍 [Retrieval Error]: {e}")
        return []
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    # Test it with a combined name
    test_word = "Farid Ahmed"
    context = retrieve_context(test_word)
    print(f"Knowledge Base Results for '{test_word}':")
    for eng, sin in context:
        print(f" - {eng} -> {sin}")