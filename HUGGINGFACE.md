# GS420 AI — Hugging Face Spaces

The recommended Space type for this repository is **Gradio**. The root `app.py` is the entry point and honors the platform-provided `PORT`.

1. Create a new Space and select **Gradio**.
2. Import/sync `nonetitle3/gs420`.
3. Set Space Variables such as:
   - `GS420_MODEL_ID=Qwen/Qwen2.5-0.5B-Instruct`
   - `GS420_DEVICE=auto`
   - `GS420_MAX_NEW_TOKENS=512`
4. For private/gated models, put `GS420_HF_TOKEN` in Space Secrets.
5. Open the Space and test the Chat tab.

Free CPU hardware is suitable for smoke testing, but model inference depends on RAM/VRAM. Heavy image/video adapters require suitable hardware. The application reports model-loading failures instead of pretending inference succeeded.

The FastAPI application is a separate entry point:
`uvicorn backend.main:app --host 0.0.0.0 --port $PORT`.
Do not start both independent servers on one port.
