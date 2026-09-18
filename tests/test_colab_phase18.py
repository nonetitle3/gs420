from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_colab_files():
    assert (ROOT/"COLAB.md").exists()
    assert (ROOT/"scripts/colab_setup.py").exists()
    assert (ROOT/"scripts/colab_check.py").exists()

def test_colab_setup_is_secret_safe():
    text=(ROOT/"scripts/colab_setup.py").read_text(encoding="utf-8")
    assert "os.environ" in text
    assert "HF_TOKEN" not in text

def test_colab_docs_cover_core_flow():
    text=(ROOT/"COLAB.md").read_text(encoding="utf-8")
    assert "T4 GPU" in text
    assert "GS420_MODEL_ID" in text
    assert "GS420_HF_TOKEN" in text
