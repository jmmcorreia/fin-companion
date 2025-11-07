from sqlmodel import select, Session
from app.dbmodel.category import Category
from typing import List

def get_catogories(session: Session) -> List[Category] | None:
    categories = session.exec(select(Category)).all()
    return list(categories) # TODO: if the number of categories is large, consider pagination


def insert_category(category: Category, session: Session) -> Category:
    session.add(category)
    session.commit()
    session.refresh(category)
    return category

    
    
    
    