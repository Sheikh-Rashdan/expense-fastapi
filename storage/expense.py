import datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import Category, Expense, User


def get_expenses(
    db: Session,
    user: User,
    limit: int,
    offset: int,
    min_amount: float,
    max_amount: float | None,
    start_date: datetime.date | None,
    end_date: datetime.date | None,
    category: Category | None,
) -> list[Expense]:
    statement = (
        select(Expense).where(Expense.user_id == user.id).offset(offset).limit(limit)
    )
    statement = statement.where(Expense.amount >= min_amount)

    if max_amount is not None:
        statement = statement.where(Expense.amount <= max_amount)
    if start_date is not None:
        statement = statement.where(Expense.date >= start_date)
    if end_date is not None:
        statement = statement.where(Expense.date <= end_date)
    if category is not None:
        statement = statement.where(Expense.category_id == category.id)

    result = db.execute(statement)
    expenses = result.scalars().all()

    return expenses


def get_expense(db: Session, expense_id: int) -> Expense | None:
    statement = select(Expense).where(Expense.id == expense_id)
    result = db.execute(statement)
    expense = result.scalar()
    return expense


def post_expense(db: Session, user: User, create_dict: dict[str, Any]) -> Expense:
    expense: Expense = Expense(user_id=user.id, **create_dict)

    db.add(expense)
    db.commit()
    db.refresh(expense)

    return expense


def delete_expense(db: Session, expense: Expense) -> None:
    db.delete(expense)
    db.commit()


def patch_expense(db: Session, expense: Expense, patch_dict: dict[str, Any]) -> Expense:
    for attr, value in patch_dict.items():
        setattr(expense, attr, value)

    db.commit()
    db.refresh(expense)

    return expense
