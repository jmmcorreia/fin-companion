from dataclasses import dataclass
from typing import Protocol

from sqlmodel import Session, select

from app.dbmodel.category import Category


class CategoryRepository(Protocol):
    def get_categories(self) -> list[Category] | None: ...
    def insert_category(self, category: Category) -> Category: ...

@dataclass
class SQLCategoryRepository:
    session: Session
    
    def get_categories(self) -> list[Category] | None:
        categories = self.session.exec(select(Category)).all()
        return list(categories) # TODO: if the number of categories is large, consider pagination


    def insert_category(self, category: Category) -> Category:
        self.session.add(category)
        self.session.flush()
        self.session.refresh(category)
        return category

    
    
    
    