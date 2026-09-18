"""GS420 AI Gradio interface."""
import gradio as gr
from backend.core.orchestrator import Orchestrator

orch = Orchestrator()

def reply(message, history, request: gr.Request):
    if not message or not message.strip():
        return ""
    session_id = getattr(request, "session_hash", None)
    return orch.chat(message.strip(), session_id=session_id)["answer"]

def build_app():
    with gr.Blocks(title="GS420 AI") as demo:
        gr.Markdown("# GS420 AI\nBengali + English AI Hub")
        with gr.Row():
            gr.Dropdown(["Auto"], value="Auto", label="Model", interactive=False)
            gr.Dropdown(["Auto", "CPU", "CUDA"], value="Auto", label="Device", interactive=False)
            gr.Checkbox(value=True, label="Memory", interactive=False)
        with gr.Tabs():
            with gr.Tab("Chat"):
                gr.ChatInterface(fn=reply, title="Ask anything", textbox=gr.Textbox(placeholder="Ask anything…"))
            with gr.Tab("Coding"):
                gr.Markdown("Coding agent and restricted Python runner are available through the API.")
            with gr.Tab("Vision"):
                gr.Markdown("Upload images through the Vision API for OCR and analysis.")
            with gr.Tab("Image"):
                gr.Markdown("Image generation, enhancement and upscaling APIs are available through the API.")
            with gr.Tab("Video"):
                gr.Markdown("Video generation adapter and frame extraction APIs are available through the API.")
            with gr.Tab("Voice"):
                gr.Markdown("Whisper STT and Piper TTS adapters are available through the API.")
            with gr.Tab("Agents"):
                gr.Markdown("Planner and controlled agents are available through the API.")
            with gr.Tab("Documents"):
                gr.Markdown("Document upload and RAG search are available through the API.")
            with gr.Tab("Memory"):
                gr.Markdown("Persistent conversation memory is available.")
            with gr.Tab("Settings"):
                gr.Markdown("Model and deployment settings are controlled by environment configuration.")
    return demo

app = build_app()

if __name__ == "__main__":
    app.launch()
