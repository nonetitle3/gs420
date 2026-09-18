# GS420 AI — Hugging Face Spaces

Phase 19 provides a Gradio Space-ready deployment path.

## Create the Space
1. Create a new Gradio Space on Hugging Face.
2. Upload or push the repository contents.
3. Choose hardware appropriate for the selected model.
4. Keep private tokens in Space Secrets, never in source files.

## Space entry point
The repository provides app.py. A Gradio Space can launch it automatically.

## Model configuration
Set the Space variable GS420_MODEL_ID, for example:
GS420_MODEL_ID=Qwen/Qwen2.5-0.5B-Instruct

Optional specialist variables:
GS420_REASONING_MODEL_ID
GS420_CODING_MODEL_ID
GS420_VISION_MODEL_ID

For private or gated models, create a Space Secret named GS420_HF_TOKEN. The application reads it from the environment.

## CPU fallback
The default model is intentionally small. If a selected model does not fit the Space hardware, choose a smaller or quantized compatible model. GS420's resource manager reports capabilities and does not claim that a large model fits free hardware.

## Local test
pip install -r requirements-hf.txt
python app.py

## API note
The Gradio Space is the user-facing deployment. The FastAPI backend remains available for deployments that run the API separately. A Gradio Space should not be assumed to expose every FastAPI route.

## Security
Never commit tokens to Git, README files, notebooks, frontend source, or launch scripts. Use Hugging Face Space Secrets or deployment environment variables.

## Resource limits
Hugging Face hardware, RAM, VRAM, storage and free-tier availability can change. Large image/video models need suitable GPU hardware or an external GPU backend.
