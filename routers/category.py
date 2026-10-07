from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import storage.category as storage
from database.db import get_db
from database.models import Category, User
from models.category import CategoryCreate, CategoryModel, CategoryPatch
from routers.user import validate_user

category_router = APIRouter(prefix="/users/{user_id}", tags=["category"])


def validate_category(category_id: int, db: Session = Depends(get_db)) -> Category:
    category: Category = storage.get_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


def validate_category_belongs_to_user(category: Category, user: User):
    if category.user_id != user.id:
        raise HTTPException(
            status_code=403,
            detail=f"User {user.id} does not own Category {category.id}",
        )


def validate_optional_category(
    category_id: int | None = None, db: Session = Depends(get_db)
) -> Category | None:
    if category_id is None:
        return None

    return validate_category(category_id, db)


def validate_unique_category(
    category_name: str, user: User, db: Session = Depends(get_db)
) -> None:
    is_duplicate: bool = storage.check_category_name_exists(db, category_name, user)
    if is_duplicate:
        raise HTTPException(
            status_code=409,
            detail=f"Category name '{category_name}' already exists for User {user.id}",
        )


@category_router.get("/categories", response_model=list[CategoryModel])
def get_categories(
    limit: int = Query(default=100, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    user: User = Depends(validate_user),
    db: Session = Depends(get_db),
) -> list[Category]:
    return storage.get_categories(db, user, limit, offset)


@category_router.get("/categories/{category_id}", response_model=CategoryModel)
def get_category(
    category: Category = Depends(validate_category), user: User = Depends(validate_user)
) -> Category:
    validate_category_belongs_to_user(category, user)

    return category


@category_router.post("/categories", response_model=CategoryModel, status_code=201)
def post_category(
    category_create: CategoryCreate,
    user: User = Depends(validate_user),
    db: Session = Depends(get_db),
) -> Category:
    validate_unique_category(category_create.name, user, db)

    return storage.post_category(db, user, category_create.model_dump())


@category_router.delete("/categories/{category_id}", status_code=204)
def delete_category(
    category: Category = Depends(validate_category),
    user: User = Depends(validate_user),
    db: Session = Depends(get_db),
) -> None:
    validate_category_belongs_to_user(category, user)

    storage.delete_category(db, category)


@category_router.patch("/categories/{category_id}", response_model=CategoryModel)
def patch_category(
    category_patch: CategoryPatch,
    category: Category = Depends(validate_category),
    user: User = Depends(validate_user),
    db: Session = Depends(get_db),
) -> Category:
    validate_category_belongs_to_user(category, user)
    validate_unique_category(category.name, user, db)

    return storage.patch_category(
        db, category, category_patch.model_dump(exclude_unset=True)
    )
