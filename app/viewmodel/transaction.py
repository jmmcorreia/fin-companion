import uuid
from datetime import datetime
from decimal import Decimal
from typing import Literal

from sqlmodel import SQLModel


class TransactionBase(SQLModel):
    occurred_on: datetime
    amount: Decimal 
    currency: str 
    category_id: uuid.UUID | None # TODO: should backend send string or UUID?
    description: str | None 
    # recurrence_id: uuid.UUID
    created_at: datetime
    
class TransactionResponse(TransactionBase):
    id: uuid.UUID

class FilterTransactions(SQLModel):
    # model_config = {"extra": "forbid"}
    
    limit: int | None = None
    offset: int | None = None
    order_by: Literal["date", "amount", "category"] | None = None
    category: str | None = None
    date_from: str | None = None
    date_to: str | None = None

# class TransactionCreate(TransactionBase):
#     password: str

# class TransactionResponse(TransactionBase):
#     id: uuid.UUID | None = None