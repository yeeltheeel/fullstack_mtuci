from datetime import date
from pydantic import BaseModel, EmailStr, ConfigDict, Field, AliasChoices

class UserOut(BaseModel):
	model_config = ConfigDict(from_attributes=True)
	user_id: int
	username: str | None
	email: EmailStr
	birthday: date | None
	avatar: str | None = Field(default=None, validation_alias=AliasChoices("avatar", "avatar_url"))

class UserCreate(BaseModel):
	username: str = Field(min_length=3, max_length=255)
	email: EmailStr
	password: str = Field(min_length=8, max_length=128)
	birthday: date | None = None

class UserUpdate(BaseModel):
	username: str | None = Field(default=None, min_length=3, max_length=255)
	email: EmailStr | None
	birthday: date | None = None
	avatar: str | None = None

class UserPasswordUpdate(BaseModel):
	current_password: str = Field(min_length=1, max_length=128)
	new_password: str = Field(min_length=4, max_length=128)

# class Token(BaseModel):
# 	access_token: str
# 	token_type: str = "Bearer"
	