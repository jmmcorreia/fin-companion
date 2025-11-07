import uuid

from sqlmodel import SQLModel


class CategoryBase(SQLModel):
    name: str
    description: str | None
    
class CategoryResponse(CategoryBase):
    id: uuid.UUID