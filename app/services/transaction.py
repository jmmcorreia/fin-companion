import uuid
from dataclasses import dataclass
from typing import List

from fastapi import HTTPException, status

from app.dbmodel.transaction import Transaction
from app.repository.transaction_repository import TransactionRepository
from app.viewmodel.transaction import (FilterTransactions, TransactionBase,
                                       TransactionResponse)
from app.viewmodel.user import UserResponse


def transaction_to_response(transaction: Transaction) -> TransactionResponse:
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

@dataclass
class TransactionService:
    repository: TransactionRepository

    def read_transactions(
        self,
        user: UserResponse,
        filter_query: FilterTransactions, # TODO: currently unused
    ) -> List[TransactionResponse]:
        transactions = self.repository.get_user_transactions(user.id)
        if not transactions:
            print("No transactions found for user:", user.id)  # TODO: add logs
            return []
        
        return [transaction_to_response(t) for t in transactions]

    def read_transaction(
        self,
        user: UserResponse,
        transaction_id: uuid.UUID,
    ) -> TransactionResponse:
        transaction = self.repository.get_user_transaction(user.id, transaction_id)
        if not transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found",
            )
        
        return transaction_to_response(transaction)

    def create_transaction(
        self,
        user: UserResponse,
        transaction_base: TransactionBase,
    ) -> TransactionResponse:
        transaction = base_to_transaction(user.id, transaction_base)
        db_transaction = self.repository.insert_transaction(transaction)
        return transaction_to_response(db_transaction)

    def remove_transaction(
        self,
        user: UserResponse,
        transaction_id: uuid.UUID,
    ) -> None:
        deleted_count = self.repository.delete_transaction(user.id, transaction_id)
        if deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found",  # user does not have auth or uuid is incorrect
            )
        return
