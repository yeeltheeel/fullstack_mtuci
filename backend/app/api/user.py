from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.crud import user as user_crud
from app.schemas.user import UserOut
from app.api.deps import get_current_user
from app.db.models import User

router = APIRouter(prefix="/users", tags=["users"])

@router.get("", response_model=list[UserOut])
async def list_users(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return await user_crud.list_users(db)

@router.get("/{user_id}", response_model=UserOut)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    user = await user_crud.get_by_id(db, user_id)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    return user

@router.get("/me", response_model=UserOut)
async def me(current: User = Depends(get_current_user)):
    return current
