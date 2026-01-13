# codex-workspace

## Docker Compose 배포 (권장)

### 사전 요구사항

- Docker (Docker Compose 포함)

### 실행 방법

```bash
cp .env.example .env
docker compose up --build
```

브라우저에서 `http://localhost` 접속 후 아래 플로우를 확인합니다.

1. 회원가입
2. 로그인
3. 파일 업로드
4. 검색
5. 다운로드

### 마이그레이션

- 백엔드는 컨테이너 시작 시 DB 연결을 재시도한 뒤 `alembic upgrade head`를 자동 실행합니다.

### 볼륨/데이터 관리

- 업로드 파일: `uploads` 볼륨 (`/data/uploads`)
- DB 데이터: `pgdata` 볼륨

```bash
docker compose down -v
```

> 위 명령은 업로드/DB 데이터를 모두 삭제합니다.

### 트러블슈팅

- **포트 충돌**: 80 포트를 사용하는 프로세스가 있으면 종료하거나 nginx 포트를 변경하세요.
- **DB 준비 전 backend 재시도**: backend는 DB가 준비될 때까지 재시도 로그를 출력합니다.
- **CORS 문제**: `.env`의 `CORS_ENABLED=true`, `CORS_ALLOW_ORIGINS=http://localhost`를 확인하세요.

## 로컬 개발 실행 순서 (참고)

### Backend 실행

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

### Frontend 실행

```bash
cd frontend
npm install
npm run dev
```

브라우저에서 로그인 → 업로드 → 검색을 확인합니다 (`http://localhost:5173`).
