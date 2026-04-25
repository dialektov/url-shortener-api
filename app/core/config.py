from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "URL Shortener API"
    database_url: str = "postgresql+psycopg://postgres:postgres@db:5432/url_shortener"
    redis_url: str = "redis://redis:6379/0"
    base_url: str = "http://localhost:8000"
    cache_ttl_seconds: int = 3600
    rate_limit_window_seconds: int = 60
    rate_limit_max_requests: int = 20

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
