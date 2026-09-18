FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    GRADIO_SERVER_NAME=0.0.0.0

WORKDIR /app
COPY requirements-hf.txt requirements.txt ./
RUN python -m pip install --upgrade pip && pip install -r requirements-hf.txt
COPY . .
RUN mkdir -p /app/data/uploads
EXPOSE 7860
CMD ["python", "app.py"]
