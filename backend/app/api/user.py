from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.api.deps import get_current_user
from app.crud import user as user_crud
from app.db.models import User
from app.schemas.user import UserOut, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])

@router.get("", response_model=list[UserOut])
async def list_users(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return await user_crud.list_users(db)

@router.get("/me", response_model=UserOut)
async def get_me(current: User = Depends(get_current_user)):
    return current

@router.patch("/me", response_model=UserOut)
async def update_me(
    payload: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current: User = Depends(get_current_user),
):
    data = payload.model_dump(exclude_unset=True)
    if "email" in data and data["email"] != current.email:
        if await user_crud.get_by_email(db, data["email"]):
            raise HTTPException(status.HTTP_409_CONFLICT, "email already taken")
    return await user_crud.update(db, current.user_id, data)

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_me(
    db: AsyncSession = Depends(get_db),
    current: User = Depends(get_current_user),
):
    await user_crud.delete(db, current.user_id)

@router.get("/{user_id}", response_model=UserOut)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user),
):
    user = await user_crud.get_by_id(db, user_id)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")
    return user

@router.patch("/{user_id}", response_model=UserOut)
async def update_user(
    user_id: int,
    payload: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current: User = Depends(get_current_user),
):
    if current.user_id != user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "cannot edit another user")
    data = payload.model_dump(exclude_unset=True)
    if "email" in data and data["email"] != current.email:
        if await user_crud.get_by_email(db, data["email"]):
            raise HTTPException(status.HTTP_409_CONFLICT, "email already taken")
    user = await user_crud.update(db, user_id, data)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current: User = Depends(get_current_user),
):
    if current.user_id != user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "cannot delete another user")
    ok = await user_crud.delete(db, user_id)
    if not ok:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "user not found")
    