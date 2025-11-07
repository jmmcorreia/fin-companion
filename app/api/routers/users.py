from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import get_current_active_user
from app.viewmodel.user import UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
def read_users_me(
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
) -> UserResponse:
    return current_user



