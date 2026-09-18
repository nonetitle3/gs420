"""GS420 AI configuration."""
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    model_id: str = Field(default="Qwen/Qwen2.5-0.5B-Instruct", alias="GS420_MODEL_ID")
    reasoning_model_id: str | None = Field(default=None, alias="GS420_REASONING_MODEL_ID")
    coding_model_id: str | None = Field(default=None, alias="GS420_CODING_MODEL_ID")
    vision_model_id: str | None = Field(default=None, alias="GS420_VISION_MODEL_ID")
    max_new_tokens: int = Field(default=512, alias="GS420_MAX_NEW_TOKENS", ge=1, le=8192)
    temperature: float = Field(default=0.7, alias="GS420_TEMPERATURE", ge=0.0, le=2.0)
    top_p: float = Field(default=0.9, alias="GS420_TOP_P", gt=0.0, le=1.0)
    max_history_messages: int = Field(default=20, alias="GS420_MAX_HISTORY_MESSAGES", ge=2, le=100)
    host: str = Field(default="0.0.0.0", alias="GS420_HOST")
    port: int = Field(default=7860, alias="GS420_PORT", ge=1, le=65535)
    device: str = Field(default="auto", alias="GS420_DEVICE")
    hf_token: str | None = Field(default=None, alias="GS420_HF_TOKEN")
    memory_db_path: str = Field(default="./data/gs420_memory.db", alias="GS420_MEMORY_DB_PATH")
    sandbox_timeout_seconds: int = Field(default=5, alias="GS420_SANDBOX_TIMEOUT_SECONDS", ge=1, le=30)
    sandbox_max_output_chars: int = Field(default=12000, alias="GS420_SANDBOX_MAX_OUTPUT_CHARS", ge=1000, le=100000)


@lru_cache
def get_settings() -> Settings:
    return Settings()
