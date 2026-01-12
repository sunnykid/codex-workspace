from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import Settings
from app.core.logging import configure_logging

settings = Settings()

configure_logging(settings.log_level)

app = FastAPI()
app.include_router(api_router)


def _resolve_cors_origins() -> list[str]:
    if settings.cors_allow_origins.strip():
        return [
            origin.strip()
            for origin in settings.cors_allow_origins.split(",")
            if origin.strip()
        ]
    if settings.env.lower() == "dev":
        return [
            "http://localhost",
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
        ]
    return []


if settings.cors_enabled:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_resolve_cors_origins(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
