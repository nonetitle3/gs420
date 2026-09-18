def test_settings_import():
 from backend.config import settings
 assert settings.app_name=="GS420 AI"
 assert settings.max_upload_mb>0
 assert settings.upload_dir

def test_gradio_factory_import():
 from gradio_ui.app import create_app
 assert callable(create_app)
