import json
import logging
import os
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.models.file import File

settings = Settings()
logger = logging.getLogger(__name__)


def _upload_root() -> Path:
    return Path(settings.upload_root)


def _resolve_storage_path(stored_path: str) -> Path:
    path = Path(stored_path)
    if path.is_absolute():
        return path
    return _upload_root() / path


def _parse_tags(raw: str | None) -> list[str] | None:
    if raw is None:
        return None
    value = raw.strip()
    if not value:
        return None
    if value.startswith("["):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            parsed = None
        if isinstance(parsed, list):
            return [str(item) for item in parsed if str(item).strip()]
    if "," in value:
        tags = [item.strip() for item in value.split(",") if item.strip()]
        return tags or None
    return [value]


def _write_upload(upload: UploadFile, destination: Path, max_bytes: int) -> int:
    destination.parent.mkdir(parents=True, exist_ok=True)
    size = 0
    try:
        with destination.open("wb") as handle:
            while True:
                chunk = upload.file.read(1024 * 1024)
                if not chunk:
                    break
                size += len(chunk)
                if size > max_bytes:
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail="Upload exceeds maximum size",
                    )
                handle.write(chunk)
    finally:
        upload.file.close()
    return size


def create_file(
    db: Session,
    owner_id: int,
    upload: UploadFile,
    tags_raw: str | None,
) -> File:
    max_bytes = settings.max_upload_mb * 1024 * 1024
    storage_name = uuid4().hex
    relative_path = Path(str(owner_id)) / storage_name
    absolute_path = _upload_root() / relative_path

    try:
        size_bytes = _write_upload(upload, absolute_path, max_bytes)
    except Exception:
        if absolute_path.exists():
            try:
                absolute_path.unlink()
            except OSError:
                logger.exception("Failed to cleanup partial upload")
        raise

    tags = _parse_tags(tags_raw)
    record = File(
        owner_id=owner_id,
        original_filename=upload.filename,
        stored_path=str(relative_path),
        content_type=upload.content_type,
        size_bytes=size_bytes,
        tags=tags,
    )
    db.add(record)
    try:
        db.commit()
    except Exception:
        db.rollback()
        if absolute_path.exists():
            try:
                absolute_path.unlink()
            except OSError:
                logger.exception("Failed to cleanup upload after DB error")
        raise
    db.refresh(record)
    return record


def list_files(
    db: Session,
    owner_id: int,
    limit: int,
    offset: int,
) -> tuple[list[File], int]:
    total = db.scalar(
        select(func.count()).select_from(File).where(File.owner_id == owner_id)
    )
    query = (
        select(File)
        .where(File.owner_id == owner_id)
        .order_by(File.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    items = db.scalars(query).all()
    return items, total or 0


def get_file_for_owner(db: Session, owner_id: int, file_id: int) -> File | None:
    query = select(File).where(File.id == file_id, File.owner_id == owner_id)
    return db.scalar(query)


def delete_file(db: Session, owner_id: int, file_id: int) -> File | None:
    record = get_file_for_owner(db, owner_id, file_id)
    if record is None:
        return None

    db.delete(record)
    db.commit()

    path = _resolve_storage_path(record.stored_path)
    try:
        os.remove(path)
    except FileNotFoundError:
        logger.warning("File already missing on disk: %s", path)
    except OSError:
        logger.exception("Failed to remove file from disk: %s", path)
    return record


def resolve_download_path(record: File) -> Path:
    path = _resolve_storage_path(record.stored_path)
    if not path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File content not found",
        )
    return path
