from dataclasses import dataclass
from typing import List

from app.dbmodel.category import Category
from app.repository.category_repository import CategoryRepository
from app.viewmodel.category import CategoryBase, CategoryResponse


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
@dataclass
class CategoryService:
    repository: CategoryRepository

    def get_categories(
        self,
    ) -> List[CategoryResponse]:
        categories = self.repository.get_categories()
        if not categories:
            print("No categories found") # TODO: add logs
            return []
        
        return [category_to_response(c) for c in categories]


    def create_category(self, category_base: CategoryBase) -> CategoryResponse:
        category = base_to_category(category_base)
        db_category = self.repository.insert_category(category)
        return category_to_response(db_category)

    
    
    
    
    



