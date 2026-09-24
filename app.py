"""GS420 AI Gradio entry point with optional Hugging Face ZeroGPU support."""
import os
import gradio as gr
from gradio_ui.app import build_app
from backend.core.orchestrator import Orchestrator

try:
    import spaces
    gpu = spaces.GPU
except ImportError:
    def gpu(fn):
        return fn

orch = Orchestrator()

@gpu
def zero_gpu_chat(message: str, session_id: str | None = None, task: str | None = None) -> str:
    """Run GS420 chat through the ZeroGPU scheduler when available."""
    if not message or not message.strip():
        return ""
    result = orch.chat(message.strip(), session_id=session_id, task=task)
    return result["answer"]

demo = build_app()
gr.api(zero_gpu_chat, api_name="chat", api_description="GS420 AI chat endpoint for the custom frontend.")

def main():
    port = int(os.getenv("PORT") or os.getenv("GRADIO_SERVER_PORT") or "7860")
    host = os.getenv("GRADIO_SERVER_NAME", "0.0.0.0")
    demo.launch(server_name=host, server_port=port, show_error=True, footer_links=["api", "gradio", "settings"])

if __name__ == "__main__":
    main()
