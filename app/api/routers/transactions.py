import uuid
from typing import Annotated, List

from fastapi import APIRouter, Depends, Query

from app.api.deps import (TransactionServiceDep, UserDep,
                          get_current_active_user)
from app.viewmodel.transaction import (FilterTransactions, TransactionBase,
                                       TransactionResponse)

router = APIRouter(prefix="/transactions", tags=["transactions"], dependencies=[Depends(get_current_active_user)])

@router.get("/")
def get_transactions(
    current_user: UserDep, 
    filter_query: Annotated[FilterTransactions, Query()],
    transaction_service: TransactionServiceDep,
) -> List[TransactionResponse]:
    
    return transaction_service.read_transactions(current_user, filter_query)

@router.get("/{transaction_id}")
def get_transaction(
    transaction_id: uuid.UUID,
    current_user: UserDep,
    transaction_service: TransactionServiceDep,
) -> TransactionResponse:
    
    return transaction_service.read_transaction(current_user, transaction_id)

@router.post("/")
def post_transaction(
    transaction: TransactionBase,
    current_user: UserDep,
    transaction_service: TransactionServiceDep,
) -> TransactionResponse:
    return transaction_service.create_transaction(current_user, transaction) 

@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: uuid.UUID,
    current_user: UserDep,
    transaction_service: TransactionServiceDep,
) -> None:
    return transaction_service.remove_transaction(current_user, transaction_id)  # Placeholder for actual transaction deletion logic 

@router.put("/{transaction_id}")
def update_transaction(
    transaction_id: uuid.UUID,
    transaction: TransactionBase,
    current_user: UserDep,
    transaction_service: TransactionServiceDep,
) -> TransactionBase:
    return transaction  # Placeholder for actual transaction update logic

@router.patch("/{transaction_id}")
def patch_transaction(
    transaction_id: uuid.UUID,
    transaction: TransactionBase,
    current_user: UserDep,
    transaction_service: TransactionServiceDep,
) -> TransactionBase:
    return transaction  # Placeholder for actual transaction patch logic