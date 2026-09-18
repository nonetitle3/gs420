# GS420 AI Troubleshooting

Model unavailable: verify model ID, access and RAM/VRAM.

CUDA unavailable: verify PyTorch/runtime; on Colab run `python scripts/colab_check.py`.

Out of memory: use smaller/quantized models or move heavy inference to suitable GPU hardware.

OCR unavailable: install Tesseract with Bengali/English language data.

Android: install Node.js, Capacitor dependencies and Android Studio/SDK.

API errors: inspect logs and use `X-Request-ID` for correlation.

Tests: run `python scripts/test_all.py`.
