# src/logic/transliterate.py
from src.db.database import get_connection

def get_phonetic_draft(text, target_lang="sindhi"):
    """
    Converts English text to a phonetic draft using the database rules.
    """
    conn = get_connection()
    cur = conn.cursor()
    
    text = text.lower().strip()
    result = ""
    col = "sindhi_mapping" if target_lang == "sindhi" else "urdu_mapping"
    
    for char in text:
        if char == " ":
            result += " "
            continue
        cur.execute(f"SELECT {col} FROM phonetic_rules WHERE letter = %s", (char,))
        row = cur.fetchone()
        result += row[0] if row else char
            
    cur.close()
    conn.close()
    return result

def get_english_phonetic(text):
    """
    Takes Sindhi or Urdu script and turns it into readable English/Roman script.
    """
    conn = get_connection()
    cur = conn.cursor()
    
    result = ""
    for char in text:
        if char == " ":
            result += " "
            continue
            
        cur.execute("""
            SELECT letter FROM phonetic_rules 
            WHERE sindhi_mapping = %s OR urdu_mapping = %s
        """, (char, char))
        
        row = cur.fetchone()
        result += row[0] if row else char
        
    cur.close()
    conn.close()
    return result.capitalize()