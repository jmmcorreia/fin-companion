from dataclasses import dataclass

from fastapi import HTTPException, status

from app.dbmodel.user import User
from app.repository.user_repository import UserRepository
from app.services.token_service import TokenService
from app.viewmodel.user import UserResponse


def user_to_response(user: User) -> UserResponse:
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
    )


@dataclass
class AuthService:
    repository: UserRepository

    def get_current_user(self, token: str) -> User:
        username = TokenService.decode_token(token)
        if not username:
            TokenService.raise_invalid_token()

        user = self.repository.get_user_by_username(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user

    def get_current_active_user(self, current_user: User) -> UserResponse:
        if getattr(current_user, "disabled", False):
            raise HTTPException(status_code=400, detail="Inactive user")
        return user_to_response(current_user)
    
    
    def get_user(self, username: str) -> User:
        user = self.repository.get_user_by_username(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user
    
    def register_user(self, user: User) -> UserResponse:
        registered_user = self.repository.register_user(user)
        return user_to_response(registered_user)
