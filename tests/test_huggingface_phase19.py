from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def test_hf_space_entrypoint():
    text=(ROOT/"app.py").read_text(encoding="utf-8")
    assert "build_ui" in text
    assert "7860" in text

def test_hf_docs_cover_secrets_and_model_config():
    text=(ROOT/"HUGGINGFACE.md").read_text(encoding="utf-8")
    assert "GS420_MODEL_ID" in text
    assert "GS420_HF_TOKEN" in text
    assert "Space Secrets" in text
    assert "free-tier availability" in text
