"""GS420 AI configuration."""
from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore")
    app_name: str = Field(default="GS420 AI", alias="GS420_APP_NAME")
    app_env: str = Field(default="production", alias="GS420_APP_ENV")
    model_id: str = Field(default="Qwen/Qwen2.5-0.5B-Instruct", alias="GS420_MODEL_ID")
    reasoning_model_id: str | None = Field(default=None, alias="GS420_REASONING_MODEL_ID")
    coding_model_id: str | None = Field(default=None, alias="GS420_CODING_MODEL_ID")
    vision_model_id: str | None = Field(default=None, alias="GS420_VISION_MODEL_ID")
    max_new_tokens: int = Field(default=512, alias="GS420_MAX_NEW_TOKENS", ge=1, le=8192)
    temperature: float = Field(default=.7, alias="GS420_TEMPERATURE", ge=0, le=2)
    top_p: float = Field(default=.9, alias="GS420_TOP_P", gt=0, le=1)
    max_history_messages: int = Field(default=20, alias="GS420_MAX_HISTORY_MESSAGES", ge=2, le=100)
    host: str = Field(default="0.0.0.0", alias="GS420_HOST")
    port: int = Field(default=7860, alias="GS420_PORT", ge=1, le=65535)
    device: str = Field(default="auto", alias="GS420_DEVICE")
    model_cache_dir: str | None = Field(default=None, alias="GS420_MODEL_CACHE_DIR")
    hf_token: str | None = Field(default=None, alias="GS420_HF_TOKEN")
    memory_db_path: str = Field(default="./data/gs420_memory.db", alias="GS420_MEMORY_DB_PATH")
    upload_dir: str = Field(default="./data/uploads", alias="GS420_UPLOAD_DIR")
    max_upload_mb: int = Field(default=25, alias="GS420_MAX_UPLOAD_MB", ge=1, le=500)
    sandbox_timeout_seconds: int = Field(default=5, alias="GS420_SANDBOX_TIMEOUT_SECONDS", ge=1, le=30)
    sandbox_max_output_chars: int = Field(default=12000, alias="GS420_SANDBOX_MAX_OUTPUT_CHARS", ge=1000, le=100000)
    admin_token: str | None = Field(default=None, alias="GS420_ADMIN_TOKEN")
    embedding_model_id: str | None = Field(default=None, alias="GS420_EMBEDDING_MODEL_ID")
    rag_enabled: bool = Field(default=True, alias="GS420_RAG_ENABLED")
    rag_top_k: int = Field(default=4, alias="GS420_RAG_TOP_K", ge=1, le=10)
    rag_semantic: bool = Field(default=True, alias="GS420_RAG_SEMANTIC")
    ocr_language: str = Field(default="ben+eng", alias="GS420_OCR_LANGUAGE")
    ocr_preprocess: str = Field(default="balanced", alias="GS420_OCR_PREPROCESS")
    ocr_min_confidence: float = Field(default=55, alias="GS420_OCR_MIN_CONFIDENCE", ge=0, le=100)
    cors_origins: str = Field(default="*", alias="GS420_CORS_ORIGINS")
    log_level: str = Field(default="INFO", alias="GS420_LOG_LEVEL")

    @property
    def db_path(self):
        return self.memory_db_path

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
Path(settings.upload_dir).mkdir(parents=True, exist_ok=True)
if settings.model_cache_dir:
    Path(settings.model_cache_dir).mkdir(parents=True, exist_ok=True)
