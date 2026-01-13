#!/usr/bin/env bash
set -euo pipefail

python - <<'PY'
import os
import time
import sys

from sqlalchemy import create_engine, text

url = os.environ.get("DATABASE_URL")
if not url:
    print("DATABASE_URL is not set", file=sys.stderr)
    sys.exit(1)

engine = create_engine(url, pool_pre_ping=True)

for attempt in range(1, 31):
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Database is ready")
        break
    except Exception as exc:  # noqa: BLE001
        print(f"Database not ready ({attempt}/30): {exc}")
        time.sleep(2)
else:
    print("Database did not become ready in time", file=sys.stderr)
    sys.exit(1)
PY

alembic upgrade head

exec uvicorn app.main:app --host 0.0.0.0 --port 8000
