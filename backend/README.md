# FastAPI Backend Skeleton

## 실행 방법

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## /health 확인

```bash
curl http://localhost:8000/health
```

예상 응답:

```json
{"status": "ok"}
```

## CORS 동작

- `CORS_ENABLED=true`일 때만 CORS 미들웨어가 활성화됩니다.
- `CORS_ALLOW_ORIGINS`가 비어 있고 `ENV=dev`인 경우에만 localhost 계열 주소가 자동 허용됩니다.
  - 예: `http://localhost`, `http://localhost:3000`, `http://127.0.0.1`, `http://127.0.0.1:3000`

## 생성된 파일 목록

- `backend/README.md`
- `backend/.env.example`
- `backend/requirements.txt`
- `backend/app/main.py`
- `backend/app/api/router.py`
- `backend/app/api/health.py`
- `backend/app/core/config.py`
- `backend/app/core/logging.py`
- `backend/app/__init__.py`
- `backend/app/api/__init__.py`
- `backend/app/core/__init__.py`
