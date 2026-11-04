from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jwt import PyJWTError

from app.db.session import get_db
from app.core.security import decode_token
from app.crud import user as user_crud
from app.db.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

_cred_error = HTTPException(
	status_code=status.HTTP_401_UNAUTHORIZED,
	detail="could not validate credentials",
	headers={"WWW-Authenticate": "Bearer"},
)

async def get_current_user(
	token: str = Depends(oauth2_scheme),
	db: AsyncSession = Depends(get_db)
) -> User:
	try:
		payload = decode_token(token, "access")
		user_id = int(payload["sub"])
	except (PyJWTError, ValueError, KeyError, TypeError):
		raise _cred_error
	
	user = await user_crud.get_by_id(db, user_id)
	if user is None:
		raise _cred_error
	return user
