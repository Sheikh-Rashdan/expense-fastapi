from sqlalchemy import select
from sqlalchemy.orm import Session
from database.models import *
from typing import Any, Optional

def get_expenses(db: Session, user: User, limit: int, offset: int) -> list[Expense]:
    statement = select(Expense).where(Expense.user == user).offset(offset).limit(limit)
    result = db.execute(statement)
    expenses = result.scalars().all()
    return expenses

def get_expense(db: Session, expense_id: int) -> Optional[Expense]:
    statement = select(Expense).where(Expense.id == expense_id)
    result = db.execute(statement)
    expense = result.scalar()
    return expense

def post_expense(db: Session, user: User, create_dict: dict[str,Any]) -> Expense:
    expense: Expense = Expense(user_id=user.id, **create_dict)

    db.add(expense)
    db.commit()
    db.refresh(expense)

    return expense

def delete_expense(db: Session, expense: Expense) -> None:
    db.delete(expense)
    db.commit()

def patch_expense(db: Session, expense: Expense, patch_dict: dict[str,Any]) -> Expense:
    for attr, value in patch_dict.items():
        setattr(expense, attr, value)

    db.commit()
    db.refresh(expense)

    return expense