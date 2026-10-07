from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from models.expense import *
from routers.user import validate_user
from database.db import get_db
from database.models import *
import storage.expense as storage

expense_router = APIRouter(tags=["expense"])

def validate_expense(expense_id: int, db: Session = Depends(get_db)) -> Expense:
    expense: Expense = storage.get_expense(db, expense_id)
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

@expense_router.get("/users/{user_id}/expenses", response_model=list[ExpenseModel])
def get_expenses(limit: int = Query(default=100, ge=1, le=100),
                   offset: int = Query(default=0, ge=0),
                   user: User = Depends(validate_user),
                   db: Session = Depends(get_db)) -> list[Expense]:
    return storage.get_expenses(db, user, limit, offset)

@expense_router.get("/expenses/{expense_id}", response_model=ExpenseModel)
def get_expense(expense: Expense = Depends(validate_expense)) -> Expense:
    return expense

@expense_router.post("/users/{user_id}/expenses", response_model=ExpenseModel, status_code=201)
def post_expense(expense_create: ExpenseCreate, user: User = Depends(validate_user), db: Session = Depends(get_db)) -> Expense:
    return storage.post_expense(db, user, expense_create.model_dump())

@expense_router.delete("/expenses/{expense_id}", status_code=204)
def delete_expense(expense: Expense = Depends(validate_expense), db: Session = Depends(get_db)) -> None:
    storage.delete_expense(db, expense)

@expense_router.patch("/expenses/{expense_id}", response_model=ExpenseModel)
def patch_expense(expense_patch: ExpensePatch, expense: Expense = Depends(validate_expense), db: Session = Depends(get_db)) -> Expense:
    return storage.patch_expense(db, expense, expense_patch.model_dump(exclude_unset=True))