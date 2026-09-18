def test_document_rejects_unknown_extension(api_client):
 r=api_client.post("/api/documents/upload",files={"file":("bad.exe",b"hello","application/octet-stream")}); assert r.status_code==400
def test_voice_rejects_unknown_extension(api_client):
 r=api_client.post("/api/voice/transcribe",files={"file":("bad.exe",b"hello","application/octet-stream")}); assert r.status_code==400
def test_calculator_validation(api_client):
 r=api_client.post("/api/tools/calculator",json={"expression":""}); assert r.status_code==422
def test_python_blocks_dangerous_import(api_client):
 r=api_client.post("/api/tools/python",json={"code":"import os\nprint(os.getcwd())"}); assert r.status_code==400
