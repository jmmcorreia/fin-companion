import uuid
from dataclasses import dataclass
from typing import List, Protocol

from sqlmodel import Session, delete, select

from app.dbmodel.transaction import Transaction


class TransactionRepository(Protocol):
    def get_user_transactions(self, user_uuid: uuid.UUID) -> List[Transaction] | None: ...
    def get_user_transaction(self, user_uuid: uuid.UUID, transaction_id: uuid.UUID) -> Transaction | None: ...
    def insert_transaction(self, transaction: Transaction) -> Transaction: ...
    def delete_transaction(self, user_uuid: uuid.UUID, transaction_id: uuid.UUID) -> int: ...

@dataclass
class SQLTransactionRepository:
    session: Session
    
    def get_user_transactions(self, user_uuid: uuid.UUID) -> List[Transaction] | None:
        transactions = self.session.exec(select(Transaction).where(Transaction.user_id == user_uuid)).all()
        return list(transactions)  # TODO: if the number of transactions is large, consider pagination

    def get_user_transaction(self, user_uuid: uuid.UUID, transaction_id: uuid.UUID) -> Transaction | None:
        transaction = self.session.exec(
            select(Transaction)
            .where(Transaction.user_id == user_uuid)
            .where(Transaction.id == transaction_id)
        ).first()
        return transaction

    def insert_transaction(self, transaction: Transaction) -> Transaction:
        self.session.add(transaction)
        self.session.commit()
        self.session.refresh(transaction)
        return transaction

    def delete_transaction(self, user_uuid: uuid.UUID, transaction_id: uuid.UUID) -> int:
        statement = (
            delete(Transaction)
            .where(Transaction.user_id == user_uuid)
            .where(Transaction.id == transaction_id)
        )
        result = self.session.exec(statement)
        self.session.commit()  # Added missing commit
        return result.rowcount
    
    
    
    