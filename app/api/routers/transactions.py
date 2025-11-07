from fastapi import APIRouter, Depends, Query
from typing import Annotated, List
import uuid


from app.viewmodel.user import UserResponse
from app.viewmodel.transaction import TransactionBase, TransactionResponse, FilterTransactions
from app.services.auth import get_current_active_user
from app.services.transaction import read_transactions, read_transaction, create_transaction, remove_transaction
from app.db.session import SessionDep

router = APIRouter(prefix="/transactions", tags=["transactions"], dependencies=[Depends(get_current_active_user)])

@router.get("/")
def get_transactions(
    current_user: Annotated[UserResponse, Depends(get_current_active_user)], 
    filter_query: Annotated[FilterTransactions, Query()],
    session: SessionDep
) -> List[TransactionResponse]:
    
    return read_transactions(current_user, filter_query, session)

@router.get("/{transaction_id}")
def get_transaction(
    transaction_id: uuid.UUID,
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
    session: SessionDep
) -> TransactionResponse:
    
    return read_transaction(current_user, transaction_id, session)

@router.post("/")
def post_transaction(
    transaction: TransactionBase,
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
    session: SessionDep
) -> TransactionResponse:
    return create_transaction(current_user, transaction, session) 

@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: uuid.UUID,
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
    session: SessionDep
) -> None:
    return remove_transaction(current_user, transaction_id, session)  # Placeholder for actual transaction deletion logic 

@router.put("/{transaction_id}")
def update_transaction(
    transaction_id: uuid.UUID,
    transaction: TransactionBase,
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
) -> TransactionBase:
    return transaction  # Placeholder for actual transaction update logic

@router.patch("/{transaction_id}")
def patch_transaction(
    transaction_id: uuid.UUID,
    transaction: TransactionBase,
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
) -> TransactionBase:
    return transaction  # Placeholder for actual transaction patch logic