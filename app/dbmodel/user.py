import uuid

from sqlmodel import Field, SQLModel  # type: ignore


class User(SQLModel, table=True):
    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    full_name: str | None = None
    disabled: bool | None = None
    hashed_password: str = Field()