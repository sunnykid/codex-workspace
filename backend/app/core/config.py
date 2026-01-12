from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    env: str = "dev"
    log_level: str = "INFO"
    cors_enabled: bool = False
    cors_allow_origins: str = ""
    database_url: str = "postgresql+psycopg://postgres:postgres@db:5432/app"
    db_echo: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )
