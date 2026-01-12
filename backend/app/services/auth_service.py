from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.security.jwt import create_access_token
from app.security.password import verify_password
from app.services.user_service import create_user, get_user_by_email

INVALID_CREDENTIALS_MESSAGE = "이메일 또는 비밀번호가 잘못되었습니다"


def register_user(db: Session, email: str, password: str):
    if len(password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="비밀번호는 최소 8자 이상이어야 합니다",
        )
    if get_user_by_email(db, email) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 사용 중인 이메일입니다",
        )
    return create_user(db, email, password)


def authenticate_user(db: Session, email: str, password: str) -> str:
    user = get_user_by_email(db, email)
    if user is None or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=INVALID_CREDENTIALS_MESSAGE,
        )
    return create_access_token(str(user.id))
