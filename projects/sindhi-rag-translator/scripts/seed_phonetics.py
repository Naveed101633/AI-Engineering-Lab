# scripts/seed_phonetics.py
import os
from src.db.database import get_connection

def seed_phonetics():
    # Format: (English_Key, Sindhi_Char, Urdu_Char)
    rules = [
        # --- Vowels (The fix for 'Noor' and 'Soomro') ---
        ('a', 'ا', 'ا'),
        ('e', 'ي', 'ے'),
        ('i', 'ي', 'ی'),
        ('o', 'و', 'و'),
        ('u', 'و', 'و'),
        ('oo', 'و', 'و'),
        ('ee', 'ي', 'ی'),
        ('aa', 'ا', 'ا'),
        
        # --- Standard Consonants ---
        ('b', 'ٻ', 'ب'), 
        ('p', 'پ', 'پ'),
        ('t', 'ت', 'ت'), 
        ('s', 'س', 'س'), 
        ('j', 'ڄ', 'ج'),
        ('ch', 'چ', 'چ'), 
        ('h', 'ه', 'ہ'), 
        ('kh', 'خ', 'خ'),
        ('d', 'ڏ', 'د'), 
        ('r', 'ر', 'ر'), 
        ('z', 'ز', 'ز'),
        ('sh', 'ش', 'ش'), 
        ('f', 'ف', 'ف'), 
        ('k', 'ڪ', 'ک'),
        ('g', 'ڳ', 'گ'), 
        ('l', 'ل', 'ل'), 
        ('m', 'م', 'م'),
        ('n', 'ن', 'ن'), 
        ('v', 'و', 'و'), 
        ('w', 'و', 'و'), 
        ('y', 'ي', 'ی'),
        
        # --- Special Sounds & Digraphs ---
        ('th', 'ٿ', 'تھ'), 
        ('ph', 'ڦ', 'پھ'), 
        ('dh', 'ڌ', 'دھ'),
        ('gh', 'گھ', 'گھ'),
        ('bh', 'ڀ', 'بھ'),
        ('jh', 'جھ', 'جھ'),
        ('rh', 'ڙ', 'ڑ'),
    ]
    
    conn = get_connection()
    cur = conn.cursor()
    
    # Optional: Clear old rules to ensure the new vowel rules take priority
    cur.execute("DELETE FROM phonetic_rules;")
    
    for eng, sin, urd in rules:
        cur.execute("""
            INSERT INTO phonetic_rules (letter, sindhi_mapping, urdu_mapping)
            VALUES (%s, %s, %s) ON CONFLICT (letter) DO NOTHING
        """, (eng, sin, urd))
    
    conn.commit()
    print("✅ Bidirectional rules updated with Vowels and Digraphs!")
    cur.close()
    conn.close()