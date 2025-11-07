from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext



from app.viewmodel.user import UserResponse
from app.repository.user_repository import get_user_by_username
from app.db.session import SessionDep
from app.viewmodel.user import UserCreate, UserResponse
from app.dbmodel.user import User
from app.services.token_service import TokenService, Token
# from app.services.token_service import oauth2_scheme

router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

@router.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep) -> Token:
    
    user = get_user_by_username(form_data.username, session)
    if not user:
        raise HTTPException(status_code=404, detail="Incorrect username or password")
    
   
    if not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(status_code=404, detail="Incorrect username or password")

    return TokenService.encode_bearer_token(user.username)


@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, session: SessionDep) -> UserResponse:
    # Hash the password and create a UserDB instance
    hashed_password = pwd_context.hash(user.password)
    user_in_db = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    session.add(user_in_db)
    session.commit()
    session.refresh(user_in_db)
    return UserResponse(
        id=user_in_db.id,
        username=user_in_db.username,
        email=user_in_db.email,
        full_name=user_in_db.full_name,
    )