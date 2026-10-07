import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import storage.expense as storage
from database.db import get_db
from database.models import Category, Expense, User
from models.expense import ExpenseCreate, ExpenseModel, ExpensePatch
from routers.category import (
    validate_category_belongs_to_user,
    validate_optional_category,
)
from routers.user import validate_user

expense_router = APIRouter(prefix="/users/{user_id}", tags=["expense"])


def validate_expense(expense_id: int, db: Session = Depends(get_db)) -> Expense:
    expense: Expense = storage.get_expense(db, expense_id)
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


def validate_expense_belongs_to_user(expense: Expense, user: User):
    if expense.user_id != user.id:
        raise HTTPException(
            status_code=403,
            detail=f"User {user.id} does not own Expense {expense.id}",
        )


def validate_date_range(
    start_date: datetime.date | None, end_date: datetime.date | None
) -> None:
    if start_date is None or end_date is None:
        return

    if start_date > end_date:
        raise HTTPException(
            status_code=422, detail="Start date is greater than end date"
        )


@expense_router.get("/expenses", response_model=list[ExpenseModel])
def get_expenses(
    limit: int = Query(default=100, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    min_amount: float = Query(default=0, ge=0),
    max_amount: float | None = Query(default=None, ge=0),
    start_date: datetime.date | None = None,
    end_date: datetime.date | None = None,
    category: Category | None = Depends(validate_optional_category),
    user: User = Depends(validate_user),
    db: Session = Depends(get_db),
) -> list[Expense]:
    validate_date_range(start_date, end_date)

    return storage.get_expenses(
        db, user, limit, offset, min_amount, max_amount, start_date, end_date, category
    )


@expense_router.get("/expenses/{expense_id}", response_model=ExpenseModel)
def get_expense(
    expense: Expense = Depends(validate_expense), user: User = Depends(validate_user)
) -> Expense:
    validate_expense_belongs_to_user(expense, user)

    return expense


@expense_router.post("/expenses", response_model=ExpenseModel, status_code=201)
def post_expense(
    expense_create: ExpenseCreate,
    user: User = Depends(validate_user),
    db: Session = Depends(get_db),
) -> Expense:
    category: Category = validate_optional_category(expense_create.category_id, db)
    if category is not None:
        validate_category_belongs_to_user(category, user)

    return storage.post_expense(db, user, expense_create.model_dump())


@expense_router.delete("/expenses/{expense_id}", status_code=204)
def delete_expense(
    expense: Expense = Depends(validate_expense),
    user: User = Depends(validate_user),
    db: Session = Depends(get_db),
) -> None:
    validate_expense_belongs_to_user(expense, user)

    storage.delete_expense(db, expense)


@expense_router.patch("/expenses/{expense_id}", response_model=ExpenseModel)
def patch_expense(
    expense_patch: ExpensePatch,
    expense: Expense = Depends(validate_expense),
    user: User = Depends(validate_user),
    db: Session = Depends(get_db),
) -> Expense:
    validate_expense_belongs_to_user(expense, user)

    return storage.patch_expense(
        db, expense, expense_patch.model_dump(exclude_unset=True)
    )
