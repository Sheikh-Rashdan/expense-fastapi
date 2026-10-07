from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from models.category import *
from routers.user import validate_user
from database.db import get_db
from database.models import *
import storage.category as storage

category_router = APIRouter(tags=["category"])

def validate_category(category_id: int, db: Session = Depends(get_db)) -> Category:
    category: Category = storage.get_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

def validate_optional_category(category_id: Optional[int] = None, db: Session = Depends(get_db)) -> Optional[Category]:
    if category_id is None: return None

    return validate_category(category_id, db)

@category_router.get("/users/{user_id}/categories", response_model=list[CategoryModel])
def get_categories(limit: int = Query(default=100, ge=1, le=100),
                   offset: int = Query(default=0, ge=0),
                   user: User = Depends(validate_user),
                   db: Session = Depends(get_db)) -> list[Category]:
    return storage.get_categories(db, user, limit, offset)

@category_router.get("/categories/{category_id}", response_model=CategoryModel)
def get_category(category: Category = Depends(validate_category)) -> Category:
    return category

@category_router.post("/users/{user_id}/categories", response_model=CategoryModel, status_code=201)
def post_category(category_create: CategoryCreate, user: User = Depends(validate_user), db: Session = Depends(get_db)) -> Category:
    return storage.post_category(db, user, category_create.model_dump())

@category_router.delete("/categories/{category_id}", status_code=204)
def delete_category(category: Category = Depends(validate_category), db: Session = Depends(get_db)) -> None:
    storage.delete_category(db, category)

@category_router.patch("/categories/{category_id}", response_model=CategoryModel)
def patch_category(category_patch: CategoryPatch, category: Category = Depends(validate_category), db: Session = Depends(get_db)) -> Category:
    return storage.patch_category(db, category, category_patch.model_dump(exclude_unset=True))