from sqlmodel import select, Session, delete
from app.dbmodel.transaction import Transaction
from typing import List
import uuid

def get_user_transactions(user_uuid: uuid.UUID, session: Session) -> List[Transaction] | None:
    transactions = session.exec(select(Transaction).where(Transaction.user_id == user_uuid)).all()
    return list(transactions) # TODO: if the number of transactions is large, consider pagination

def get_user_transaction(user_uuid: uuid.UUID, transaction_id: uuid.UUID, session: Session) -> Transaction | None:
    transaction = session.exec(select(Transaction).where(Transaction.user_id == user_uuid, Transaction.id == transaction_id)).first()
    return transaction

def insert_transaction(transaction: Transaction, session: Session) -> Transaction:
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction


def delete_transaction(user_uuid: uuid.UUID, transaction_id: uuid.UUID, session: Session) -> int:
    statement = delete(Transaction).where(Transaction.user_id == user_uuid, Transaction.id == transaction_id)
    result = session.exec(statement)
    return result.rowcount
    
    
    
    