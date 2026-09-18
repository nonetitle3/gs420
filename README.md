# GS420 AI

Open-source-first modular AI hub for Bengali and English: chat, coding, voice, vision/OCR, image/video adapters, agents, tools, documents, memory, PWA, Android, Colab and Hugging Face.

## Quick start
pip install -r requirements.txt
python app.py

API: `uvicorn backend.main:app --host 0.0.0.0 --port 8000`

## Testing
`python scripts/test_all.py`

## Documentation
See ARCHITECTURE.md, INSTALL.md, MODEL_GUIDE.md, AGENTS.md, SECURITY.md, TROUBLESHOOTING.md, TESTING.md, COLAB.md, HUGGINGFACE.md, ANDROID.md and PHASED_GENERATION_GUIDE.md.

No OpenAI API key is required. Model backends are replaceable and hardware-aware.
