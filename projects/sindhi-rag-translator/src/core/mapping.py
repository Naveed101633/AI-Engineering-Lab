# src/core/mapping.py

# Forward Maps: Script to English (Predictable)
BASE_MAP = {
    "ا": "a", "ب": "b", "پ": "p", "ت": "t", "ٹ": "tt", "ث": "s",
    "ج": "j", "چ": "ch", "ح": "h", "خ": "kh", "د": "d", "ڈ": "dd",
    "ذ": "z", "ر": "r", "ڑ": "rr", "ز": "z", "ژ": "zh", "س": "s",
    "ش": "sh", "ص": "s", "ض": "z", "ط": "t", "ظ": "z", "ع": "a",
    "غ": "gh", "ف": "f", "ق": "q", "ک": "k", "گ": "g", "ل": "l",
    "م": "m", "ن": "n", "و": "o", "ہ": "h", "ی": "i", "ے": "e",
    "آ": "aa", "ء": "'"
}

SINDHI_EXTRA = {
    "ٻ": "bb", "ٿ": "th", "ٽ": "tt", "ٺ": "tth", "ڄ": "jj", 
    "ڇ": "chh", "ڌ": "dh", "ڏ": "dd", "ڊ": "dd", "ڍ": "ddh", 
    "ڦ": "ph", "ڪ": "k", "ڳ": "gg", "ڱ": "ng", "ڻ": "n"
}

SINDHI_TO_ENG = {**BASE_MAP, **SINDHI_EXTRA}
URDU_TO_ENG = BASE_MAP

# Reverse Maps: English to Script (Canonical Defaults Only)
# We do NOT use dictionary comprehension here to avoid data loss.
ENG_TO_SCRIPT_DEFAULT = {
    "a": "ا", "b": "ب", "p": "پ", "t": "ت", "d": "د", 
    "r": "ر", "s": "س", "sh": "ش", "kh": "خ", "gh": "غ", 
    "f": "ف", "q": "ق", "k": "ک", "g": "گ", "l": "ل", 
    "m": "م", "n": "ن", "h": "ہ", "y": "ی", "o": "و", "i": "ی"
}

def rule_based_transliterate(text: str, source_lang: str, target_lang: str) -> str:
    """
    Directional transliteration. 
    NOTE: English -> Script uses canonical defaults; 
    complex phonemes (sh, kh) are refined in the AI layer.
    """
    if not text:
        return ""
    
    # Selection Logic
    if target_lang == "english":
        mapping = SINDHI_TO_ENG if source_lang == "sindhi" else URDU_TO_ENG
    else:
        mapping = ENG_TO_SCRIPT_DEFAULT
    
    # Process text
    result = "".join([mapping.get(char, char) for char in text.lower()])
    
    return result.strip().capitalize() if target_lang == "english" else result.strip()