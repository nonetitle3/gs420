def test_gradio_app_factory():
 from gradio_ui.app import build_app
 assert build_app() is not None
