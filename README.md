# GS420 AI

Open-source-first modular AI hub: chat, coding, vision, OCR, image/video adapters, voice, agents, tools, documents, memory, PWA and Android/Colab/Hugging Face deployment paths.

## Quick start
pip install -r requirements.txt
python app.py

## Hugging Face Spaces
Use app.py as the Gradio entry point. Configure GS420_MODEL_ID and optional specialist model variables in Space Variables. Put private Hugging Face credentials in Space Secrets as GS420_HF_TOKEN. See HUGGINGFACE.md.

## Google Colab
See COLAB.md and run python scripts/colab_setup.py.

## API
uvicorn backend.main:app --host 0.0.0.0 --port 8000

GS420 has no required OpenAI API key. Model backends are replaceable and hardware-aware fallbacks are preferred.
