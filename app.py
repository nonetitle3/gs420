"""
GS420 AI - Main application entry point.

Starts the FastAPI backend and mounts the Gradio UI.
"""

import uvicorn
from gradio_ui.app import create_app
from backend.main import app as fastapi_app
from backend.config import get_settings

settings = get_settings()

# Mount Gradio under /ui while keeping the API available at /api.
gradio_app = create_app()
from gradio.routes import mount_gradio_app
application = mount_gradio_app(
    app=fastapi_app,
    blocks=gradio_app,
    path="/ui",
)

def main() -> None:
    uvicorn.run(
        application,
        host=settings.host,
        port=settings.port,
        reload=False,
    )

if __name__ == "__main__":
    main()
