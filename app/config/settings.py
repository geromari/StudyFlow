"""Application configuration using Pydantic Settings."""

from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Telegram Bot
    bot_token: str = Field(default="TEST_BOT_TOKEN", alias="BOT_TOKEN")

    # Database
    database_url: str = Field(
        default="sqlite+aiosqlite:///studyflow.db",
        alias="DATABASE_URL",
    )

    # Redis
    redis_url: str = Field(default="redis://localhost:6379/0", alias="REDIS_URL")

    # AI Configuration (OpenAI compatible)
    ai_api_key: str = Field(default="", alias="AI_API_KEY")
    ai_base_url: str = Field(default="https://api.openai.com/v1", alias="AI_BASE_URL")
    ai_model: str = Field(default="gpt-4o-mini", alias="AI_MODEL")
    ai_max_input_chars: int = Field(default=2000, alias="AI_MAX_INPUT_CHARS")
    ai_max_output_tokens: int = Field(default=1000, alias="AI_MAX_OUTPUT_TOKENS")
    ai_rate_limit_per_minute: int = Field(default=10, alias="AI_RATE_LIMIT_PER_MINUTE")

    # Admin Telegram IDs
    admin_ids: list[int] = Field(default_factory=list, alias="ADMIN_IDS")

    # App options
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    default_language: str = Field(default="uz", alias="DEFAULT_LANGUAGE")
    default_timezone: str = Field(default="UTC", alias="DEFAULT_TIMEZONE")
    max_pdf_size_mb: int = Field(default=200, alias="MAX_PDF_SIZE_MB")

    @field_validator("admin_ids", mode="before")
    @classmethod
    def parse_admin_ids(cls, v: Any) -> list[int]:
        if isinstance(v, str):
            if not v.strip():
                return []
            return [int(x.strip()) for x in v.split(",") if x.strip().isdigit()]
        elif isinstance(v, (list, tuple, set)):
            return [int(x) for x in v]
        return []


settings = Settings()
