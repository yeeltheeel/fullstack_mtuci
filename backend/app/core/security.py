from datetime import datetime, timedelta, timezone
from typing import Literal
import jwt
from pwdlib import PasswordHash

from app.core.config import settings

ALGORITHM = "HS256"
TokenType = Literal["access", "refresh"]

password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
	return password_hash.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
	return password_hash.verify(plain, hashed)

def _encode(subject: str, kind: TokenType, expires: timedelta) -> str:
	now = datetime.now(timezone.utc)
	payload = {
		"sub": subject, 
		"type": kind, 
		"iat": now, 
		"exp": now + expires
	}
	return jwt.encode(
		payload, 
		settings.SECRET_KEY, 
		algorithm=ALGORITHM
	)

def create_access_token(subject: str) -> str:
	return _encode(
		subject, "access",
		timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MIN),
	)

def create_refresh_token(subject: str) -> str:
	return _encode(
		subject, "refresh",
		timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
	)

def decode_token(token: str, expected_type: TokenType) -> dict:
	payload = jwt.decode(
		token, 
		settings.SECRET_KEY, 
		algorithms=[ALGORITHM]
	)
	if payload.get("type") != expected_type:
		raise ValueError(f"expected {expected_type} token, got {payload.get('type')!r}")
	return payload
