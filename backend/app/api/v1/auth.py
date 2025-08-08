from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt

from app.core.config import settings
from app.core.deps import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, Token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.vk_user_id == payload.vk_user_id).first()
    if not user:
        user = User(vk_user_id=payload.vk_user_id, username=payload.username)
        db.add(user)
        db.commit()
        db.refresh(user)

    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": str(user.id), "vk_user_id": payload.vk_user_id, "exp": expire}
    token = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALG)
    return Token(access_token=token)