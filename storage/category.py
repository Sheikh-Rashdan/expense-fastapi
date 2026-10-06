from sqlalchemy import select
from sqlalchemy.orm import Session
from database.models import *
from typing import Any

def get_categories(db: Session, user: User, limit: int, offset: int) -> list[Category]:
    statement = select(Category).where(Category.user == user).offset(offset).limit(limit)
    result = db.execute(statement)
    categories = result.scalars().all()
    return categories

def get_category(db: Session, category_id: int) -> Category:
    statement = select(Category).where(Category.id == category_id)
    result = db.execute(statement)
    category = result.scalar()
    return category

def post_category(db: Session, user: User, create_dict: dict[str,Any]) -> Category:
    category: Category = Category(user_id=user.id, **create_dict)

    db.add(category)
    db.commit()
    db.refresh(category)

    return category

def delete_category(db: Session, category: Category) -> None:
    db.delete(category)
    db.commit()

def patch_category(db: Session, category: Category, patch_dict: dict[str,Any]) -> Category:
    for attr, value in patch_dict.items():
        setattr(category, attr, value)

    db.commit()
    db.refresh(category)

    return category