# GS420 AI
Open-source-first AI hub for Bengali + English chat, coding, memory, voice and multimodal workflows.

## Test everything
From the repository root, run one command:

python scripts/test_all.py

Equivalent:
python -m pytest -q tests

This runs the complete pytest suite, including API, routing, memory, coding, voice and capability smoke tests. Model-heavy inference is intentionally not downloaded during tests; unavailable optional models are tested through graceful adapters rather than pretending real inference succeeded.
