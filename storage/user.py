from sqlalchemy import select
from sqlalchemy.orm import Session
from database.models import *
from typing import Any

def get_users(db: Session) -> list[User]:
    statement = select(User)
    result = db.execute(statement)
    users = result.scalars().all()
    return users

def get_user(db: Session, user_id: int) -> User:
    statement = select(User).where(User.id == user_id)
    result = db.execute(statement)
    user = result.scalar()
    return user

def post_user(db: Session, user_dict: dict[str,Any]) -> User:
    user: User = User(**user_dict)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def delete_user(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()