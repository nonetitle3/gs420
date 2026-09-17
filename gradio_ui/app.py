"""GS420 AI Gradio application factory."""
import gradio as gr
from backend.config import get_settings
from backend.core.orchestrator import AIOrchestrator
from gradio_ui.chat import create_chat_ui

def create_app() -> gr.Blocks:
    settings = get_settings()
    return create_chat_ui(AIOrchestrator(settings))
