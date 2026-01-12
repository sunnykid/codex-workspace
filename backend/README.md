# Backend (FastAPI Skeleton)

## Requirements
- Python 3.11

## Local setup (venv)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Environment variables
Create a `.env` file in `backend/` (or export variables in your shell):
```bash
ENV=local
LOG_LEVEL=INFO
CORS_ENABLED=false
CORS_ALLOW_ORIGINS=http://localhost:3000
```

A full template is available at `.env.example`.

## Run (development)
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Optional:
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Health check
```bash
curl http://localhost:8000/health
```
