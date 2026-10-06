from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.user import *
from database.db import get_db
import storage.user as storage

user_router = APIRouter(prefix="/users", tags=["user"])

@user_router.get("", response_model=list[UserModel])
def get_users(db: Session = Depends(get_db)):
    return storage.get_users(db)