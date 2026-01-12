import logging

from fastapi import APIRouter, Query
from sqlalchemy import text

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health")
def health_check(db: int | None = Query(default=None)) -> dict:
    response = {"status": "ok"}
    if db == 1:
        try:
            from app.db.session import engine

            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            response["db"] = "ok"
        except Exception:
            logger.exception("Database health check failed")
            response["db"] = "error"
    return response
