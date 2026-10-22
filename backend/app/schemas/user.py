from datetime import date
from pydantic import BaseModel, EmailStr, ConfigDict, Field

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: int
    username: str | None
    email: EmailStr
    birthday: date | None
    avatar: str | None

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=255)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    birthday: date | None = None

class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=255)
    birthday: date | None = None
    avatar: str | None = None

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    