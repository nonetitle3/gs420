"""GS420 AI Gradio chat interface."""
from __future__ import annotations
import gradio as gr
from backend.core.orchestrator import AIOrchestrator

def create_chat_ui(orchestrator: AIOrchestrator) -> gr.Blocks:
    def new_session():
        return orchestrator.new_session(), [], "New conversation started."

    def clear_session(session_id: str):
        if session_id:
            orchestrator.clear_history(session_id)
        return orchestrator.new_session(), [], "Conversation cleared."

    def respond(message, chat_history, session_id, temperature, max_new_tokens):
        if not message or not message.strip():
            yield "", chat_history, session_id, "Please enter a message."
            return
        if not session_id:
            session_id = orchestrator.new_session()
        updated = list(chat_history)
        updated.append({"role": "user", "content": message})
        updated.append({"role": "assistant", "content": ""})
        yield "", updated, session_id, "Generating..."
        accumulated = ""
        try:
            for chunk in orchestrator.stream_chat(
                session_id, message,
                temperature=temperature,
                max_new_tokens=max_new_tokens,
            ):
                accumulated += chunk
                updated[-1] = {"role": "assistant", "content": accumulated}
                yield "", updated, session_id, "Generating..."
            yield "", updated, session_id, "Ready"
        except Exception as exc:
            updated[-1] = {"role": "assistant", "content": f"GS420 AI error:\n\n{exc}"}
            yield "", updated, session_id, "Error"

    with gr.Blocks(title="GS420 AI") as demo:
        gr.Markdown("# GS420 AI\n\n**Open-model AI platform**\n\nBengali + English • Hugging Face • Streaming Chat")
        with gr.Row():
            with gr.Column(scale=3):
                chatbot = gr.Chatbot(label="Conversation", type="messages", height=550)
                message = gr.Textbox(label="Message", placeholder="Ask GS420 AI anything...", lines=3)
                with gr.Row():
                    send = gr.Button("Send", variant="primary")
                    new_chat = gr.Button("New Chat")
                    clear = gr.Button("Clear")
            with gr.Column(scale=1):
                gr.Markdown("### Model\n\nHugging Face\n\n### Language\n\nবাংলা / English\n\n### Mode\n\nAuto\n\n### Phase\n\nPhase 1")
                temperature = gr.Slider(0.0, 1.5, value=0.7, step=0.05, label="Temperature")
                max_new_tokens = gr.Slider(32, 2048, value=512, step=32, label="Max new tokens")
                status = gr.Markdown("Ready")
        inputs = [message, chatbot, session_id := gr.State("")]
        outputs = [message, chatbot, session_id, status]
        send.click(respond, inputs=[message, chatbot, session_id, temperature, max_new_tokens], outputs=outputs)
        message.submit(respond, inputs=[message, chatbot, session_id, temperature, max_new_tokens], outputs=outputs)
        new_chat.click(new_session, outputs=[session_id, chatbot, status])
        clear.click(clear_session, inputs=[session_id], outputs=[session_id, chatbot, status])
    return demo
