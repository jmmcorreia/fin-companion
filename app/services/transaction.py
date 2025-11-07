# from typing import Annotated
from fastapi import HTTPException, status
from typing import List
import uuid

from app.db.session import SessionDep
# from app.dbmodel.user import User
from app.viewmodel.user import UserResponse
from app.viewmodel.transaction import FilterTransactions, TransactionBase, TransactionResponse
from app.repository.transaction_repository import get_user_transactions, get_user_transaction, insert_transaction, delete_transaction
from app.dbmodel.transaction import Transaction

## Mapping Layer ###
# TODO: mapping is simple, keep in service layer. If mapping increases, move to mapper layer
def transation_to_response(transaction: Transaction) -> TransactionResponse:
    return TransactionResponse(
        id=transaction.id,
        amount=transaction.amount,
        occurred_on=transaction.occurred_on,
        description=transaction.description,
        currency=transaction.currency,
        category_id=transaction.category_id,
        created_at=transaction.created_at,
    )
    
def base_to_transaction(user_id: uuid.UUID, transaction: TransactionBase) -> Transaction:
    return Transaction(
        amount=transaction.amount,
        user_id=user_id,
        occurred_on=transaction.occurred_on,
        description=transaction.description,
        currency=transaction.currency,
        category_id=transaction.category_id,
        created_at=transaction.created_at,
    )

## Service Layer ###

def read_transactions(
    user: UserResponse,
    filter_query: FilterTransactions,
    session: SessionDep,
) -> List[TransactionResponse]:
    transactions = get_user_transactions(user.id, session)
    if not transactions:
        print("No transactions found for user:", user.id) # TODO: add logs
        return []
    
    view_transactions: List[TransactionResponse] = []
    for t in transactions:
        view_transactions.append(transation_to_response(t))
    return view_transactions

def read_transaction(
    user: UserResponse,
    transaction_id: uuid.UUID,
    session: SessionDep,
) -> TransactionResponse:
    transaction = get_user_transaction(user.id, transaction_id, session)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found",
        )
    
    return transation_to_response(transaction)

def create_transaction(user: UserResponse, transaction_base: TransactionBase, session: SessionDep) -> TransactionResponse:
    transaction = base_to_transaction(user.id, transaction_base)
    db_transaction = insert_transaction(transaction, session)
    return transation_to_response(db_transaction)

def remove_transaction(user: UserResponse, transaction_id: uuid.UUID, session: SessionDep) -> None:
    deleted_count = delete_transaction(user.id, transaction_id, session)
    if deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found", # user does not have auth or uuid is incorrect. We do not want to expose if uuid exists in another user space
        )
    return 
    
    
    
    
    
    



