from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.search import FileSummary, SearchResponse
from app.security.jwt import get_current_user
from app.services.search_service import search_files

router = APIRouter(prefix="/search", tags=["search"])


@router.get("", response_model=SearchResponse)
def search(
    q: str | None = Query(default=None, description="부분 파일명 검색"),
    tag: str | None = Query(default=None, description="tags 배열 포함 여부"),
    owner_email: str | None = Query(default=None, description="현재 버전에서는 미지원"),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if owner_email is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="owner_email filter not supported in this version",
        )

    items, total = search_files(
        db=db,
        owner_id=current_user.id,
        q=q,
        tag=tag,
        limit=limit,
        offset=offset,
    )
    summaries = [
        FileSummary(
            id=item.id,
            original_filename=item.original_filename,
            content_type=item.content_type,
            size_bytes=item.size_bytes,
            tags=item.tags,
            created_at=item.created_at,
        )
        for item in items
    ]
    return SearchResponse(items=summaries, total=total, limit=limit, offset=offset)
