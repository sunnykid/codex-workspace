from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.file import FileListItem, FileListResponse, FileUploadResponse
from app.security.jwt import get_current_user
from app.services.file_service import (
    create_file,
    delete_file,
    get_file_for_owner,
    list_files,
    resolve_download_path,
)

router = APIRouter(prefix="/files", tags=["files"])


@router.post("", response_model=FileUploadResponse, status_code=status.HTTP_201_CREATED)
def upload_file(
    upload: UploadFile = File(...),
    tags: str | None = Form(default=None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    record = create_file(db=db, owner_id=current_user.id, upload=upload, tags_raw=tags)
    return FileUploadResponse(
        file_id=record.id,
        original_filename=record.original_filename,
        size_bytes=record.size_bytes,
        created_at=record.created_at,
        tags=record.tags,
    )


@router.get("", response_model=FileListResponse)
def list_my_files(
    limit: int = Query(default=50, ge=1),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    limit = min(limit, 100)
    items, total = list_files(
        db=db,
        owner_id=current_user.id,
        limit=limit,
        offset=offset,
    )
    summaries = [
        FileListItem(
            id=item.id,
            original_filename=item.original_filename,
            content_type=item.content_type,
            size_bytes=item.size_bytes,
            tags=item.tags,
            created_at=item.created_at,
        )
        for item in items
    ]
    return FileListResponse(items=summaries, total=total, limit=limit, offset=offset)


@router.get("/{file_id}/download")
def download_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    record = get_file_for_owner(db=db, owner_id=current_user.id, file_id=file_id)
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    path = resolve_download_path(record)
    return FileResponse(path, filename=record.original_filename)


@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file_route(
    file_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    record = delete_file(db=db, owner_id=current_user.id, file_id=file_id)
    if record is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    return None
