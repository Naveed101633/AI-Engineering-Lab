import chainlit as cl
import sys
import os
import re

# 1. Ensure the script can find the 'src' folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# 2. Add the missing imports
from src.ai.refiner import translate_with_context, client # Import client from refiner
from src.rag.retriever import retrieve_context
from src.logic.transliterate import get_english_phonetic # Import the logic you just wrote

def is_latin(text):
    # Checks if text is English/Roman alphabet
    return bool(re.match(r'^[a-zA-Z0-9\s,.\'!?]+$', text))

@cl.on_chat_start
async def start():
    await cl.Message(
        content="🕌 **Sindhi-Urdu-English AI Translator**\nConnected to **PostgreSQL** (104,890 rows)."
    ).send()


# src/ui/chat_app.py

@cl.on_message
async def main(message: cl.Message):
    user_input = message.content.strip()
    source_elements = []
    
    # 1. Start the "Processing" animation
    async with cl.Step(name="🔍 AI is thinking...", type="run") as step:
        if is_latin(user_input):
            # English -> Sindhi Logic
            step.input = f"Searching database for: {user_input}"
            
            translation = translate_with_context(user_input, "english", "sindhi")
            label = "Sindhi Translation"
            
            # Check for DB matches to show evidence
            context_data = retrieve_context(user_input)
            if context_data:
                source_text = "\n".join([f"- **{eng}**: {sin}" for eng, sin in context_data])
                source_elements.append(cl.Text(name="Database Evidence", content=source_text, display="inline"))
            else:
                label = "Phonetic Transliteration (Name/New Word)"
        
        else:
            # Sindhi/Urdu -> English Logic
            step.input = f"Analyzing script: {user_input}"
            translation = translate_with_context(user_input, "sindhi", "english")
            label = "English Transliteration"

        # Update step when finished
        step.output = "Translation complete!"

    # 2. Send the final result
    await cl.Message(
        content=f"**{label}:**\n### {translation}",
        elements=source_elements
    ).send()