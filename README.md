# codex-workspace

## Authentication (JWT)

### Environment

Set `SECRET_KEY` (required) and optionally `ACCESS_TOKEN_EXPIRE_MINUTES` (defaults to 30).

```
SECRET_KEY=your-secret
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Register

```
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"strongpassword"}'
```

### Login

```
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"strongpassword"}'
```

### Using the JWT

```
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"strongpassword"}' | jq -r '.access_token')

auth_header="Authorization: Bearer ${TOKEN}"
# Use ${auth_header} with protected endpoints.
```

## 로컬 개발 실행 순서

1) Backend 실행

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export SECRET_KEY=your-secret
export CORS_ENABLED=true
export CORS_ALLOW_ORIGINS=http://localhost:5173
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

2) Frontend 실행

```bash
cd frontend
npm install
npm run dev
```

3) 브라우저에서 로그인 → 업로드 → 검색

- 접속: `http://localhost:5173`
- 회원가입 후 로그인
- 파일 업로드/내 파일 목록 확인
- 검색 페이지에서 파일명/태그 검색
