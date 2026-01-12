from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def _split_origins(value: str | List[str]) -> List[str]:
    if isinstance(value, list):
        return value
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


class Settings(BaseSettings):
    env: str = Field(default="local")
    log_level: str = Field(default="INFO")
    cors_enabled: bool = Field(default=False)
    cors_allow_origins: List[str] = Field(default_factory=list)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @field_validator("cors_allow_origins", mode="before")
    @classmethod
    def parse_cors_allow_origins(cls, value: str | List[str]) -> List[str]:
        return _split_origins(value)


@lru_cache
def get_settings() -> Settings:
    return Settings()
