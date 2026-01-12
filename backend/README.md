# FastAPI Backend Skeleton

## 실행 방법

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 로컬 PostgreSQL 실행 예시

```bash
docker run --name local-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=app \
  -p 5432:5432 \
  -d postgres:15
```

## DATABASE_URL 예시

- 로컬 실행 (호스트 OS에서 실행할 때):

```bash
DATABASE_URL=postgresql+psycopg://postgres:postgres@127.0.0.1:5432/app
```

- Docker Compose 등 컨테이너 환경에서 실행할 때:

```bash
DATABASE_URL=postgresql+psycopg://postgres:postgres@db:5432/app
```

> 컨테이너 환경에서는 `localhost`가 앱 컨테이너 자신을 가리키므로, DB 서비스 이름(예: `db`)을 사용하세요.

## Alembic 마이그레이션

```bash
alembic revision --autogenerate -m "init"
alembic upgrade head
```

### 적용 확인 방법

```bash
psql "postgresql://postgres:postgres@127.0.0.1:5432/app" -c "\\dt"
```

## /health 확인

```bash
curl http://localhost:8000/health
```

예상 응답:

```json
{"status": "ok"}
```

DB 연결 확인이 필요할 때는 `db=1`을 추가합니다.

```bash
curl "http://localhost:8000/health?db=1"
```

예상 응답:

```json
{"status": "ok", "db": "ok"}
```

## /search 사용법

`/search`는 인증이 필요하며, 기본적으로 현재 사용자(owner_id)의 파일만 검색합니다.

- `q`: 파일명 부분 검색 (`original_filename ILIKE "%q%"`)
- `tag`: tags 배열에 포함된 값으로 필터 (tags는 JSON 배열, 예: `["a", "b"]`)
- `owner_email`: 이번 버전에서는 지원하지 않으며 요청 시 400 오류를 반환합니다.
- `limit`: 기본 50, 최대 100
- `offset`: 기본 0

### curl 예시

```bash
curl -H "Authorization: Bearer <token>" \\
  "http://localhost:8000/search?q=report"
```

```bash
curl -H "Authorization: Bearer <token>" \\
  "http://localhost:8000/search?tag=finance"
```

```bash
curl -H "Authorization: Bearer <token>" \\
  "http://localhost:8000/search?q=report&tag=finance"
```

### 인덱스 참고

- 기본 인덱스: `(owner_id, created_at)` 복합 인덱스, `tags` JSONB에 대한 GIN 인덱스
- 추가 최적화(선택): `pg_trgm` 확장 + `original_filename`에 대한 GIN 트라이그램 인덱스

## /files 사용법

`/files`는 인증이 필요하며, 기본적으로 현재 사용자(owner_id)의 파일만 조회/다운로드/삭제합니다.

### 저장 위치

- 업로드 루트는 `UPLOAD_ROOT` 환경변수로 지정하며 기본값은 `/data/uploads`입니다.
- 실제 저장 경로는 `{UPLOAD_ROOT}/{user_id}/{uuid4}` 형식으로 생성됩니다.

### 환경 변수

```bash
UPLOAD_ROOT=/data/uploads
MAX_UPLOAD_MB=50
```

### 테스트용 curl 예시

1) 로그인 후 토큰 획득

```bash
curl -X POST http://localhost:8000/auth/login \\
  -H "Content-Type: application/json" \\
  -d '{"email":"user@example.com","password":"password"}'
```

2) 업로드 (multipart)

```bash
curl -X POST http://localhost:8000/files \\
  -H "Authorization: Bearer <token>" \\
  -F "upload=@/path/to/report.pdf" \\
  -F 'tags=["finance","q1"]'
```

3) 목록 조회

```bash
curl -H "Authorization: Bearer <token>" \\
  "http://localhost:8000/files?limit=50&offset=0"
```

4) 다운로드

```bash
curl -L -H "Authorization: Bearer <token>" \\
  "http://localhost:8000/files/1/download" \\
  -o report.pdf
```

5) 삭제

```bash
curl -X DELETE -H "Authorization: Bearer <token>" \\
  "http://localhost:8000/files/1"
```

## CORS 동작

- `CORS_ENABLED=true`일 때만 CORS 미들웨어가 활성화됩니다.
- `CORS_ALLOW_ORIGINS`가 비어 있고 `ENV=dev`인 경우에만 localhost 계열 주소가 자동 허용됩니다.
  - 예: `http://localhost`, `http://localhost:3000`, `http://127.0.0.1`, `http://127.0.0.1:3000`
  - Vite 개발 서버 예시: `http://localhost:5173`

### 로컬 프론트엔드 연동 예시

```bash
CORS_ENABLED=true
CORS_ALLOW_ORIGINS=http://localhost:5173
```

## 생성된 파일 목록

- `backend/README.md`
- `backend/.env.example`
- `backend/requirements.txt`
- `backend/alembic.ini`
- `backend/alembic/env.py`
- `backend/alembic/script.py.mako`
- `backend/alembic/versions/0001_init_models.py`
- `backend/app/main.py`
- `backend/app/api/router.py`
- `backend/app/api/health.py`
- `backend/app/core/config.py`
- `backend/app/core/logging.py`
- `backend/app/db/base.py`
- `backend/app/db/session.py`
- `backend/app/models/user.py`
- `backend/app/models/file.py`
- `backend/app/models/__init__.py`
- `backend/app/__init__.py`
- `backend/app/api/__init__.py`
- `backend/app/core/__init__.py`
