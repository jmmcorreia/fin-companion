from typing import Annotated
from fastapi import Depends, HTTPException, status

# from app.api.routers.auth import oauth2_scheme
from app.services.token_service import oauth2_scheme
from app.db.session import SessionDep
from app.dbmodel.user import User
from app.viewmodel.user import UserResponse
from app.repository.user_repository import get_user_by_username
from app.services.token_service import TokenService

def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep
) -> User:
    username = TokenService.decode_token(token)
    if not username:
        TokenService.raise_invalid_token()

    user = get_user_by_username(username, session) # type: ignore
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserResponse:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
    )