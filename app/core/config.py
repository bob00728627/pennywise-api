from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PENNYWISE_", env_file=".env", extra="ignore")

    app_name: str = "Pennywise API"
    secret_key: str = "dev-secret-change-me"
    algorithm: str = "HS256"
    access_token_minutes: int = 60 * 24
    database_url: str = "sqlite:///./pennywise.db"
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:4173"]


@lru_cache
def get_settings() -> Settings:
    return Settings()
