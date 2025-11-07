from fastapi import APIRouter, Depends
from typing import Annotated

from app.viewmodel.user import UserResponse
from app.services.auth import get_current_active_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
def read_users_me(
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
) -> UserResponse:
    return current_user



