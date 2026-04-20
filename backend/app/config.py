from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Application
    APP_NAME: str = "HireFlow"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    SECRET_KEY: str = "change-me-in-production"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://hireflow:hireflow_dev@localhost:5432/hireflow"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # AI API Keys
    DEEPSEEK_API_KEY: str | None = None
    OPENAI_API_KEY: str | None = None

    # WeCom
    WECOM_CORP_ID: str | None = None
    WECOM_AGENT_ID: str | None = None
    WECOM_SECRET: str | None = None
    WECOM_TOKEN: str | None = None
    WECOM_ENCODING_AES_KEY: str | None = None

    # ASR
    ASR_PROVIDER: str = "whisper"
    XUNFEI_APP_ID: str | None = None
    XUNFEI_API_KEY: str | None = None
    XUNFEI_API_SECRET: str | None = None

    # File Upload
    UPLOAD_DIR: str = "./data/uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    def model_post_init(self, __context):
        """Post initialization to parse CORS_ORIGINS if it's a string."""
        if isinstance(self.CORS_ORIGINS, str):
            self.CORS_ORIGINS = [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


settings = get_settings()
