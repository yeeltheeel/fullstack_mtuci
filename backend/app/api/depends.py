from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.db.models import User
from app.core.security import decode_token

DB = Annotated[AsyncSession, Depends(get_db)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")


async def get_current_user(db: DB, token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    sub = decode_token(token)
    if not sub:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")
    user = (await db.execute(select(User).where(User.email == sub))).scalar_one_or_none()
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User not found")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]