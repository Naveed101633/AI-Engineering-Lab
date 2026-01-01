# test_rag.py
from src.ai.refiner import translate_with_context

# Test a sentence that is likely in your 100k dataset
test_sentence = "توهان جو نالو ڇا آهي؟"

print("⏳ Searching database and asking Gemini...")
result = translate_with_context(test_sentence, "english", "sindhi")

print(f"\nTarget Sentence: {test_sentence}")
print(f"RAG Translation: {result}")