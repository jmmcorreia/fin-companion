from typing import List
from app.db.session import SessionDep
from app.viewmodel.category import CategoryBase, CategoryResponse
from app.repository.category_repository import get_catogories, insert_category
from app.dbmodel.category import Category

## Mapping Layer ###
# TODO: mapping is simple, keep in service layer. If mapping increases, move to mapper layer
def category_to_response(category: Category) -> CategoryResponse:
    return CategoryResponse(
        id=category.id,
        name=category.name,
        description=category.description,
    )
    
    
def base_to_category(category: CategoryBase) -> Category:
    return Category(
        name=category.name,
        description=category.description,
    )

## Service Layer ###
def read_categorries(
    session: SessionDep,
) -> List[CategoryResponse]:
    categories = get_catogories(session)
    if not categories:
        print("No categories found") # TODO: add logs
        return []
    
    view_categories: List[CategoryResponse] = []
    for c in categories:
        view_categories.append(category_to_response(c))
    return view_categories


def create_category(category_base: CategoryBase, session: SessionDep) -> CategoryResponse:
    category = base_to_category(category_base)
    db_category = insert_category(category, session)
    return category_to_response(db_category)

    
    
    
    
    



