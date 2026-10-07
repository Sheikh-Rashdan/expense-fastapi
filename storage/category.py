from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models import Category, User


def get_categories(db: Session, user: User, limit: int, offset: int) -> list[Category]:
    statement = (
        select(Category).where(Category.user_id == user.id).offset(offset).limit(limit)
    )
    result = db.execute(statement)
    categories = result.scalars().all()
    return categories


def get_category(db: Session, category_id: int) -> Category | None:
    statement = select(Category).where(Category.id == category_id)
    result = db.execute(statement)
    category = result.scalar()
    return category


def post_category(db: Session, user: User, create_dict: dict[str, Any]) -> Category:
    category: Category = Category(user_id=user.id, **create_dict)

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def delete_category(db: Session, category: Category) -> None:
    db.delete(category)
    db.commit()


def patch_category(
    db: Session, category: Category, patch_dict: dict[str, Any]
) -> Category:
    for attr, value in patch_dict.items():
        setattr(category, attr, value)

    db.commit()
    db.refresh(category)

    return category


def check_category_name_exists(db: Session, category_name: str, user: User) -> bool:
    statement = (
        select(Category.name)
        .distinct()
        .where(Category.user_id == user.id, Category.name == category_name)
    )
    result = db.execute(statement)
    is_duplicate = result.scalar() is not None

    return is_duplicate
