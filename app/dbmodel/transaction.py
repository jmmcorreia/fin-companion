import uuid
from decimal import Decimal
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel # type: ignore
from sqlalchemy import Column, DateTime, func

class Transaction(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    user_id: uuid.UUID = Field(index=True, foreign_key="user.id")
    occurred_on: datetime = Field(index=True)
    amount: Decimal  = Field(default=0, max_digits=14, decimal_places=2)
    currency: str = Field(max_length=3, default="EUR")
    category_id: uuid.UUID | None = Field(default=None, foreign_key="category.id")
    description: str | None = Field(default=None, max_length=255)
    # recurrence_id: uuid.UUID | None = Field(default=None, foreign_key="recurrence_templates.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False))