from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from database.models import Category, Expense, User


def get_users(db: Session, limit: int, offset: int) -> list[User]:
    statement = select(User).offset(offset).limit(limit)
    result = db.execute(statement)
    users = result.scalars().all()
    return users


def get_user(db: Session, user_id: int) -> User | None:
    statement = select(User).where(User.id == user_id)
    result = db.execute(statement)
    user = result.scalar()
    return user


def post_user(db: Session, create_dict: dict[str, Any]) -> User:
    user: User = User(**create_dict)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def delete_user(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()


def patch_user(db: Session, user: User, patch_dict: dict[str, Any]) -> User:
    for attr, value in patch_dict.items():
        setattr(user, attr, value)

    db.commit()
    db.refresh(user)

    return user


def get_user_summary(db: Session, user: User) -> dict[str, Any]:
    response = {}

    statement = select(func.sum(Expense.amount), func.count(Expense.amount)).where(
        Expense.user_id == user.id
    )
    result = db.execute(statement).one()
    response["total_expenses"] = result[0] or 0
    response["expense_count"] = result[1] or 0

    statement = (
        select(Category.name, func.sum(Expense.amount))
        .where(Expense.user_id == user.id)
        .join(Category)
        .group_by(Category.name)
    )
    result = db.execute(statement)
    response["by_category"] = {k: v for k, v in result.all()}

    return response
