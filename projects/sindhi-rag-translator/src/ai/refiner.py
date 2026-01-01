# src/ai/refiner.py
import os
from google import genai
from dotenv import load_dotenv
from src.rag.retriever import retrieve_context
from src.logic.transliterate import get_phonetic_draft, get_english_phonetic

load_dotenv()

# Initialize Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def translate_with_context(original_text: str, source_lang: str, target_lang: str) -> str:
    """
    Primary Entry Point: Logic flow is Dictionary -> Phonetic Mapping -> AI Refinement.
    """
    # 1. Database Lookup (RAG)
    context_data = retrieve_context(original_text)
    
    if context_data:
        context_str = "\n".join([f"{eng}: {sin}" for eng, sin in context_data])
        prompt = f"""
        TASK: Translate the text below using the provided Database context.
        CONTEXT:
        {context_str}
        
        TEXT TO TRANSLATE: {original_text}
        
        Provide only the {target_lang} translation.
        """
        try:
            response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
            return response.text.strip()
        except Exception as e:
            print(f"❌ [AI Translation Error]: {e}")

    # 2. Fallback to Phonetic Logic
    print(f"🔍 '{original_text}' not in DB. Processing with Phonetic Waterfall...")
    
    if source_lang.lower() == "english":
        draft = get_phonetic_draft(original_text, target_lang)
    else:
        draft = get_english_phonetic(original_text)

    # 3. Final AI Clean-up
    return get_ai_refinement(original_text, draft, source_lang, target_lang)

def get_ai_refinement(original_text: str, rule_based_output: str, source_lang: str, target_lang: str) -> str:
    """
    Professional Transliteration Refiner.
    Fixes messy phonetic drafts (e.g., 'نooر' -> 'نور').
    """
    if not original_text or not rule_based_output:
        return rule_based_output

    # Enhanced Prompt for cleaner results
    prompt = f"""
    ROLE: Expert Linguist specializing in {source_lang} and {target_lang} transliteration.
    
    INPUT:
    - Original Name: {original_text}
    - Phonetic Draft: {rule_based_output}
    
    TASK:
    1. Clean the 'Phonetic Draft' into standard {target_lang} script.
    2. Remove any remaining English characters (like 'o', 'u', 'e') and replace with proper {target_lang} vowels.
    3. Ensure standard cultural spelling for names/surnames.
    
    CONSTRAINT: Output ONLY the corrected script. No extra text or explanations.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        refined = response.text.strip()

        # Efficiency Check: If AI hallucinates a sentence, fallback to rule-based
        if len(refined.split()) > 4: 
            return rule_based_output

        return refined.capitalize() if target_lang.lower() == "english" else refined

    except Exception as e:
        print(f"❌ [Gemini Refinement Error]: {e}")
        return rule_based_output