from typing import List

from fastapi import APIRouter, Depends

from app.api.deps import CategoryServiceDep, get_current_active_user
from app.viewmodel.category import CategoryBase, CategoryResponse

router = APIRouter(prefix="/categories", tags=["categories"], dependencies=[Depends(get_current_active_user)])
# TODO: RBAC ?

@router.get("/")
def get_categories(
    category_service: CategoryServiceDep,
) -> List[CategoryResponse]:
    
    return category_service.get_categories()


@router.post("/")
def post_category(
    category: CategoryBase,
    category_service: CategoryServiceDep,
) -> CategoryResponse:
    return category_service.create_category(category) 
