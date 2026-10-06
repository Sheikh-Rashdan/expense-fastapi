from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.user import *
from database.db import get_db
from database.models import *
import storage.user as storage

user_router = APIRouter(prefix="/users", tags=["user"])

def validate_user(user_id: int, db: Session = Depends(get_db)) -> User:
    user: User = storage.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.get("", response_model=list[UserModel])
def get_users(db: Session = Depends(get_db)) -> list[User]:
    return storage.get_users(db)

@user_router.get("/{user_id}", response_model=UserModel)
def get_user(user: User = Depends(validate_user)) -> User:
    return user

@user_router.post("", response_model=UserModel, status_code=201)
def post_user(user_create: UserCreate, db: Session = Depends(get_db)) -> User:
    return storage.post_user(db, user_create.model_dump())