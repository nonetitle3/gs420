"""GS420 AI Gradio application."""
import gradio as gr
from backend.config import get_settings
from backend.core.orchestrator import Orchestrator

def create_app():
    orch=Orchestrator()
    with gr.Blocks(title="GS420 AI") as demo:
        gr.Markdown("# GS420 AI\nModel: Auto · Memory: Enabled")
        with gr.Tab("Chat"):
            chat=gr.Chatbot(type="messages")
            msg=gr.Textbox(label="Message",placeholder="Ask anything...")
            def respond(text,history):
                result=orch.chat(text)
                history=history or []
                history += [{"role":"user","content":text},{"role":"assistant","content":result["answer"]}]
                return history,""
            msg.submit(respond,[msg,chat],[chat,msg])
        for name in ["Coding","Vision","Image","Video","Voice","Agents","Documents","Memory","Settings"]:
            with gr.Tab(name): gr.Markdown(f"{name} capability is available through the FastAPI adapters.")
    return demo
