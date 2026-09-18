# GS420 AI — Deployment

## Render backend

This repository includes a Render Blueprint at `render.yaml`.

1. Open Render and choose **New → Blueprint**.
2. Connect the GitHub repository `nonetitle3/gs420`.
3. Select branch `main`.
4. Render reads `render.yaml` and creates the `gs420-ai-api` web service.
5. After deployment, verify `/health`, `/`, and `/docs`.

### Resource note

The free CPU service is suitable for deployment smoke tests and API health checks. Local Hugging Face model inference may exceed free-instance RAM depending on the model/runtime. If chat inference fails with memory/runtime errors, move inference to a GPU-capable backend or use a larger instance.

### Frontend

The React frontend uses `VITE_API_URL`. Set it to the deployed backend URL when building the frontend:

```
VITE_API_URL=https://YOUR-RENDER-SERVICE.onrender.com
```

Do not put secrets in frontend environment variables.
