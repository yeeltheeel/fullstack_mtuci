from datetime import date
from pydantic import BaseModel, EmailStr, Field, AliasChoices

class UserOut(BaseModel):
    id: int = Field(validation_alias=AliasChoices("user_id", "id"))
    username: str
    birthday: date | None = None
    email: EmailStr
    avatar: str | None = None
    logged: bool = False

    model_config = {"from_attributes": True, "populate_by_name": True}


class UserCreate(BaseModel):
    username: str
    birthday: date | None = None
    email: EmailStr
    avatar: str | None = None
    pass_: str = Field(min_length=6)