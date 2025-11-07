from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

SECRET_KEY = "your-secret-key"  # TODO: load from environment
ALGORITHM = "HS256"

# Shared OAuth2 scheme for dependency injection
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenService:
    @staticmethod
    def encode_token(username: str, expires_delta: timedelta | None = None) -> str:
        payload: dict[str, object] = {"sub": username}
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        payload["exp"] = int(expire.timestamp())
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM) # type: ignore
    
    @staticmethod
    def encode_bearer_token(username: str, expires_delta: timedelta | None = None) -> Token:
        token = TokenService.encode_token(username, expires_delta)
        return Token(access_token=token, token_type="bearer")

    @staticmethod
    def decode_token(token: str) -> str:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # type: ignore
            return payload.get("sub")
        except jwt.PyJWTError as e:
            # TODO add logging here
            print("Token decoding failed", e)
            return ""

    @staticmethod
    def raise_invalid_token():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
