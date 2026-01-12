from datetime import datetime

from pydantic import BaseModel


class FileSummary(BaseModel):
    id: int
    original_filename: str
    content_type: str | None
    size_bytes: int
    tags: list[str] | None
    created_at: datetime

    class Config:
        orm_mode = True


class SearchResponse(BaseModel):
    items: list[FileSummary]
    total: int
    limit: int
    offset: int
