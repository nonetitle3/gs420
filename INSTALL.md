# GS420 AI Installation

Python 3.10+ is recommended.

```bash
python -m venv .venv
pip install -r requirements.txt
python app.py
```

API-only: `uvicorn backend.main:app --host 0.0.0.0 --port 8000`

Start with a small model on CPU. Configure model/device values through environment settings. Keep secrets out of Git.
