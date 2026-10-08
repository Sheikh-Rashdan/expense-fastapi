from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import storage
from database.models import Category, Expense, User
from models.category import CategoryModel
from models.expense import ExpenseModel
from models.user import UserModel
from routers.user import get_current_user, get_db

admin_router = APIRouter(prefix="/admin", tags=["admin"])


def validate_admin(user: User) -> None:
    if not user.is_admin:
        raise HTTPException(status_code=403, detail=f"User {user.id} is not an admin")


@admin_router.get("/users", response_model=list[UserModel])
def get_all_users(
    user: User = Depends(get_current_user),
    limit: int = Query(default=100, ge=1),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> list[User]:
    validate_admin(user)

    return storage.user.get_users(db, limit, offset)


@admin_router.get("/categories", response_model=list[CategoryModel])
def get_all_categories(
    user: User = Depends(get_current_user),
    limit: int = Query(default=100, ge=1),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> list[Category]:
    validate_admin(user)

    return storage.category.get_all_categories(db, limit, offset)


@admin_router.get("/expenses", response_model=list[ExpenseModel])
def get_all_expenses(
    user: User = Depends(get_current_user),
    limit: int = Query(default=100, ge=1),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> list[Expense]:
    validate_admin(user)

    return storage.expense.get_all_expenses(db, limit, offset)
