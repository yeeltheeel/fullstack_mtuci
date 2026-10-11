from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.depends import DB, CurrentUser
from app.crud import user as crud
from app.core.security import verify_password, make_token
from app.schemas.user import UserCreate, UserOut

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("/register", response_model=UserOut, status_code=201)
async def register(payload: UserCreate, db: DB):
    if await crud.get_by_email(db, payload.email):
        raise HTTPException(400, "Email already registered")
    user = await crud.create_user(db, payload)
    return crud.to_user_out(user, logged=True)


@router.post("/login", response_model=dict)
async def login(form: OAuth2PasswordRequestForm = Depends(), db: DB = None):
    user = await crud.get_by_email(db, form.username)
    if not user or not verify_password(form.password, user.pass_):
        raise HTTPException(401, "Bad credentials")
    return {"access_token": make_token(user.email), "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
async def me(current: CurrentUser):
    return crud.to_user_out(current, logged=True)