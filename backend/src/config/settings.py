"""Application settings using Pydantic Settings."""

from functools import lru_cache

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Application
    app_name: str = Field(default="HealthFlow API")
    app_version: str = Field(default="1.0.0")
    debug: bool = Field(default=False)
    environment: str = Field(default="development")

    # Database
    database_url: PostgresDsn = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/healthflow"
    )
    database_echo: bool = Field(default=False)

    # Security
    secret_key: str  # No default - must be provided via env
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30)
    refresh_token_expire_days: int = Field(default=7)

    # Supabase
    supabase_url: str = Field(default="")
    supabase_key: str = Field(default="")
    supabase_jwt_secret: str = Field(default="")

    # CORS
    cors_origins: list[str] = Field(default=["http://localhost:3000"])

    # Logging
    log_level: str = Field(default="INFO")
    json_logs: bool = Field(default=False)


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
