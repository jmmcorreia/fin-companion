from sqlmodel import SQLModel
import uuid


class CategoryBase(SQLModel):
    name: str
    description: str | None
    
class CategoryResponse(CategoryBase):
    id: uuid.UUID