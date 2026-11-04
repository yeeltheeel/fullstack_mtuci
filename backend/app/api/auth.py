from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.crud import user as user_crud
from app.core.security import (
	verify_password,
	create_access_token,
	create_refresh_token,
	decode_token
)
from app.schemas.user import UserOut, UserCreate
from app.schemas.tokens import Token, TokenRefresh

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, db: AsyncSession = Depends(get_db)):
	if await user_crud.get_by_email(db, payload.email):
		raise HTTPException(status.HTTP_409_CONFLICT, "email already registered")
	return await user_crud.create(db, payload.model_dump())

@router.post("/login", response_model=Token)
async def login(
	form: OAuth2PasswordRequestForm = Depends(),
	db: AsyncSession = Depends(get_db),
):
	user = await user_crud.get_by_email(db, form.username)
	if user is None or not verify_password(form.password, user.password_hash):
		raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid credentials")
	sub = str(user.user_id)
	return Token(
		access_token=create_access_token(sub),
		refresh_token=create_refresh_token(sub),
	)

@router.post("/refresh", response_model=Token)
async def refresh(body: TokenRefresh, db: AsyncSession = Depends(get_db)):
	try:
		payload = decode_token(body.refresh_token, "refresh")
		user_id = int(payload["sub"])
	except (Exception,):  # PyJWTError | ValueError | KeyError | TypeError
		raise HTTPException(
			status.HTTP_401_UNAUTHORIZED,
			"invalid refresh token",
			headers={"WWW-Authenticate": "Bearer"},
		)

	user = await user_crud.get_by_id(db, user_id)
	if user is None:
		raise HTTPException(status.HTTP_401_UNAUTHORIZED, "invalid refresh token")

	sub = str(user.user_id)
	return Token(
		access_token=create_access_token(sub),
		refresh_token=create_refresh_token(sub),  
	)
