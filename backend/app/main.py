from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import Settings
from app.core.logging import configure_logging

settings = Settings()

configure_logging(settings.log_level)

app = FastAPI()


def _resolve_cors_origins() -> list[str]:
    # 1) 명시 설정이 있으면 그걸 최우선으로 사용
    if settings.cors_allow_origins and settings.cors_allow_origins.strip():
        return [
            origin.strip()
            for origin in settings.cors_allow_origins.split(",")
            if origin.strip()
        ]

    # 2) dev 환경 기본 허용 (WSL IP 접속까지 고려)
    if settings.env.lower() == "dev":
        return [
            "http://localhost",
            "http://localhost:3000",
            "http://localhost:5173",
            "http://127.0.0.1",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
            # WSL에서 Windows 브라우저로 접근하는 경우를 위한 추가
            # (고정 IP가 아니면 .env에 cors_allow_origins로 넣는 것을 권장)
            "http://172.20.29.248:5173",
        ]

    return []


# ✅ 미들웨어는 라우터 등록 전에 추가 (중요)
if settings.cors_enabled:
    origins = _resolve_cors_origins()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# ✅ 그 다음 라우터 등록
app.include_router(api_router)

