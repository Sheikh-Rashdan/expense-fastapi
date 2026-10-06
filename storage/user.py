from sqlalchemy import select
from sqlalchemy.orm import Session
from database.models import *

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