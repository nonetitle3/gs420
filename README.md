# GS420 AI

Open-source-first Bengali/English AI hub. The deployment architecture is **free-first**: no OpenAI API, paid inference endpoint, paid GPU, paid Docker host, or mandatory subscription is required.

## Deployment modes

1. **Static PWA** — GitHub Pages or another static host. The React/Vite app builds to `frontend/dist` and does not need Python to serve the shell.
2. **FastAPI runtime** — local or a free web service such as Render's free tier when available. Set `VITE_API_URL` at frontend build time.
3. **Hugging Face ZeroGPU** — optional Gradio runtime when the account/Space is eligible. Set `VITE_GRADIO_URL` and `VITE_RUNTIME_MODE=gradio`.
4. **Google Colab** — temporary GPU runtime using `notebooks/GS420_Colab.ipynb`.
5. **Local CPU/GPU** — completely independent of hosted services.

Free resources are dynamic and can sleep, disconnect, queue, or become unavailable. GS420 must report runtime/model unavailability instead of fabricating an answer.

## Local development

```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

## Static frontend

```bash
cd frontend
npm install
set VITE_API_URL=https://YOUR-BACKEND-URL
npm run build
```

For PowerShell use `$env:VITE_API_URL="https://YOUR-BACKEND-URL"`. GitHub Pages uses repository variables in `.github/workflows/pages.yml`.

## ZeroGPU

Create a Hugging Face **Gradio Space** only if your account is eligible for ZeroGPU. The Space entry point is `app.py`. The app exposes a Gradio API named `/chat` backed by `spaces.GPU` when the `spaces` package is available. Set Space variable `GS420_MODEL_ID` and, for gated/private models only, a Space Secret `GS420_HF_TOKEN`. No OpenAI key is used.

ZeroGPU is not unlimited; when GPU capacity/quota is unavailable, the runtime can queue or fail. GS420 does not treat that as a successful inference.

## Colab

Open `notebooks/GS420_Colab.ipynb`. It clones the repository, installs dependencies, detects CUDA, selects CPU/GPU, and starts FastAPI on port 8000. Colab sessions are temporary; do not store durable user data only on the runtime disk.

## Model configuration

`GS420_MODEL_ID` is lazy-loaded on the first chat request. `GS420_DEVICE=auto` uses CUDA when available and otherwise CPU. `GS420_DTYPE=auto` is reserved for future dtype tuning. If all model candidates fail, the API returns an explicit model-unavailable response.

## API

- GET `/health`
- GET `/docs`
- POST `/api/chat`
- POST `/api/chat/stream`

Example:

```json
{"message":"বাংলায় উত্তর দাও।","session_id":"demo"}
```

## Security/free-tier notes

Keep `.env` out of Git. Do not commit tokens. Set CORS to the exact frontend origin for public deployment instead of `*`. The Python code runner is defense-in-depth, not a hostile multi-tenant sandbox; do not expose it to untrusted users without an isolated container/VM.

## Validation status

Repository configuration has been audited. Static frontend deployment was previously verified. Current public backend/ZeroGPU/Colab inference URLs are **not claimed verified** until exercised in their actual free runtime.
