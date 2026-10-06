from sqlalchemy import select
from sqlalchemy.orm import Session
from database.models import *

def get_users(db: Session) -> list[User]:
    statement = select(User)
    result = db.execute(statement)
    users = result.scalars().all()
    return users