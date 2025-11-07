from fastapi import APIRouter, Depends
from typing import List


from app.viewmodel.category import CategoryBase, CategoryResponse
from app.services.auth import get_current_active_user
from app.services.category import read_categorries, create_category
from app.db.session import SessionDep

router = APIRouter(prefix="/categories", tags=["categories"], dependencies=[Depends(get_current_active_user)])
# TODO: RBAC ?

@router.get("/")
def get_categories(
    session: SessionDep
) -> List[CategoryResponse]:
    
    return read_categorries(session)


@router.post("/")
def post_category(
    category: CategoryBase,
    session: SessionDep
) -> CategoryResponse:
    return create_category(category, session) 
