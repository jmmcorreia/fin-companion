from typing import Annotated
from fastapi import Depends
from app.db.session import get_session, SessionDep
from app.repository.transaction_repository import SQLTransactionRepository
from app.repository.category_repository import SQLCategoryRepository
from app.repository.user_repository import SQLUserRepository
from app.services.transaction import TransactionService
from app.services.category import CategoryService
from app.services.auth import AuthService
from app.viewmodel.user import UserResponse
from app.services.token_service import oauth2_scheme
from app.dbmodel.user import User


def get_auth_service(
    session: Annotated[SessionDep, Depends(get_session)],
) -> AuthService:
    repo = SQLUserRepository(session)
    return AuthService(repo)

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]

def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_service: AuthServiceDep,
) -> User:
    
    return auth_service.get_current_user(token)

def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
    auth_service: AuthServiceDep,
) -> UserResponse:
    return auth_service.get_current_active_user(current_user)

UserDep = Annotated[UserResponse, Depends(get_current_active_user)]


def get_transaction_service(
    session: Annotated[SessionDep, Depends(get_session)],
) -> TransactionService:
    repo = SQLTransactionRepository(session)
    return TransactionService(repo)

TransactionServiceDep = Annotated[TransactionService, Depends(get_transaction_service)]


def get_categories_service(
    session: Annotated[SessionDep, Depends(get_session)],
) -> CategoryService:
    
    repo = SQLCategoryRepository(session)
    return CategoryService(repo)

CategoryServiceDep = Annotated[CategoryService, Depends(get_categories_service)]




