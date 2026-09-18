"""Hugging Face Spaces / local Gradio entry point for GS420 AI."""
from gradio_ui.app import build_ui

demo=build_ui()

if __name__=="__main__":
    demo.launch(server_name="0.0.0.0",server_port=7860)
