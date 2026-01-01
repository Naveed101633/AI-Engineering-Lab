# 🔬 AI-Engineering-Lab-Project_01

A specialized Monorepo for Natural Language Processing (NLP), RAG architectures, and linguistic tools for low-resource languages.

## 🏗️ Project Portfolio

### 1. [Sindhi-Urdu Hybrid RAG Translator](./projects/sindhi-rag-translator)
**A localized transliteration engine solving phonetic hallucinations in standard LLMs.**

* **Core Logic:** Implements a "Waterfall" architecture: 
    1. **Vector/Keyword Search:** Querying a 104k+ row PostgreSQL dictionary.
    2. **Phonetic Mapping:** Rule-based fallback for Out-of-Vocabulary (OOV) terms.
    3. **AI Refinement:** Gemini 2.0 Flash integration for cultural spelling correction.
* **Tech Stack:** Python, PostgreSQL, Google GenAI SDK, Chainlit.
* **Data Scale:** 104,890 linguistic pairs.

---

## 🛠️ Global Lab Configuration
This repository uses a Monorepo structure to share utilities across projects. 

### Prerequisites
- Python 3.11+
- Docker (for PostgreSQL)
- Gemini API Key

---
*Maintained by [Naveed Ahmed]. Focused on building bridges between regional languages and modern AI.*
