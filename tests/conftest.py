import os,tempfile
import pytest
os.environ.setdefault("GS420_MEMORY_DB_PATH",os.path.join(tempfile.gettempdir(),"gs420-test-memory.db"))
os.environ.setdefault("GS420_UPLOAD_DIR",os.path.join(tempfile.gettempdir(),"gs420-test-uploads"))
@pytest.fixture
def api_client():
 from fastapi.testclient import TestClient
 from backend.main import app
 return TestClient(app)
