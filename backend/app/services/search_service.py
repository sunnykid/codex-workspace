from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.file import File


def search_files(
    db: Session,
    owner_id: int,
    q: str | None,
    tag: str | None,
    limit: int,
    offset: int,
):
    filters = [File.owner_id == owner_id]
    if q:
        filters.append(File.original_filename.ilike(f"%{q}%"))
    if tag:
        filters.append(File.tags.contains([tag]))

    total = db.scalar(select(func.count()).select_from(File).where(*filters)) or 0

    query = (
        select(File)
        .where(*filters)
        .order_by(File.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    items = db.scalars(query).all()
    return items, total
