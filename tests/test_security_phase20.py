from backend.security import safe_filename,validate_upload
def test_filename_is_confined():
    assert "/" not in safe_filename("../../secret.txt")
def test_upload_validation():
    assert validate_upload(b"ok","a.txt",1,{".txt"})=="a.txt"
