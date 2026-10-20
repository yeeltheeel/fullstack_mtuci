from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jwt import PyJWTError

from app.db.session import get_db
from app.core.security import decode_access_token
from app.crud import user as user_crud
from app.db.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        user_id = int(payload.get("sub"))
    except (PyJWTError, TypeError, ValueError):
        raise credentials_error

    user = await user_crud.get_by_id(db, user_id)
    if user is None or not user.is_active:
        raise credentials_error
    return user
