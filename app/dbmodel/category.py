import uuid

from sqlmodel import Field, SQLModel  # type: ignore


class Category(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    name: str = Field(index=True, unique=True, max_length=100)
    description: str | None = Field(default=None, max_length=255)