from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext

from app.api.deps import AuthServiceDep
from app.dbmodel.user import User
from app.services.token_service import Token, TokenService
from app.viewmodel.user import UserCreate, UserResponse

# from app.services.token_service import oauth2_scheme

router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

@router.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], auth_service: AuthServiceDep) -> Token:
    
    user = auth_service.get_user(form_data.username)
    if not user:
        raise HTTPException(status_code=404, detail="Incorrect username or password")
    
    if not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=404, detail="Incorrect username or password")

    return TokenService.encode_bearer_token(user.username)


@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, auth_service: AuthServiceDep) -> UserResponse:
    # This business logic should ideally be in the service layer
    hashed_password = pwd_context.hash(user.password)
    user_in_db = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    return auth_service.register_user(user_in_db)
