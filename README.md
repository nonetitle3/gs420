# GS420 AI
Open-source/open-weight-first Bengali/English modular AI hub.

## Phase 1 foundation
FastAPI chat API, Gradio UI, Hugging Face model adapter, conversation history, Bengali/English responses, SSE streaming, configuration and graceful model errors.

## Run
python -m venv .venv
pip install -r requirements.txt
cp .env.example .env
python start.py

API docs: /docs

## Frontend
cd frontend
npm install
npm run build

Set VITE_API_URL to the FastAPI base URL when the frontend is hosted separately.

## Model policy
No OpenAI API key is required. Default inference uses a configurable Hugging Face model. Heavy models should run on suitable GPU/Colab hardware.
