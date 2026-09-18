"""GS420 AI Gradio entry point."""
import os
from gradio_ui.app import build_app

demo = build_app()

def main():
    port = int(os.getenv("PORT") or os.getenv("GRADIO_SERVER_PORT") or "7860")
    host = os.getenv("GRADIO_SERVER_NAME", "0.0.0.0")
    demo.launch(server_name=host, server_port=port, show_error=True)

if __name__ == "__main__":
    main()
