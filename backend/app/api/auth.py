from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.crud import user as user_crud
from app.core.security import verify_password, create_access_token
from app.schemas.user import UserOut, UserCreate, Token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await user_crud.get_by_username(db, payload.username)
    if existing:
        raise HTTPException(status.HTTP_409_CONFLICT, "Username already taken")
    return await user_crud.create(db, payload.username, payload.password)

@router.post("/login", response_model=Token)
async def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    # OAuth2 form uses `username` field; we map it to our username column
    user = await user_crud.get_by_username(db, form.username)
    if user is None or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
    token = create_access_token(subject=str(user.user_id))
    return Token(access_token=token)
