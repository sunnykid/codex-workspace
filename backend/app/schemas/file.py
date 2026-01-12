from datetime import datetime

from pydantic import BaseModel


class FileUploadResponse(BaseModel):
    file_id: int
    original_filename: str
    size_bytes: int
    created_at: datetime
    tags: list[str] | None

    class Config:
        orm_mode = True


class FileListItem(BaseModel):
    id: int
    original_filename: str
    content_type: str | None
    size_bytes: int
    tags: list[str] | None
    created_at: datetime

    class Config:
        orm_mode = True


class FileListResponse(BaseModel):
    items: list[FileListItem]
    total: int
    limit: int
    offset: int
