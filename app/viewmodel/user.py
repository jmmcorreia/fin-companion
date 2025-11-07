import uuid

from sqlmodel import SQLModel


# TODO: Use pydantic models for user input and output?
class UserBase(SQLModel):
    username: str
    email: str
    full_name: str | None = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: uuid.UUID