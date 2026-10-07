from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import storage.user as storage
from database.db import get_db
from database.models import *
from models.summary import *
from models.user import *

user_router = APIRouter(prefix="/users", tags=["user"])


def validate_user(user_id: int, db: Session = Depends(get_db)) -> User:
    user: User = storage.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.get("", response_model=list[UserModel])
def get_users(
    limit: int = Query(default=100, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> list[User]:
    return storage.get_users(db, limit, offset)


@user_router.get("/{user_id}", response_model=UserModel)
def get_user(user: User = Depends(validate_user)) -> User:
    return user


@user_router.post("", response_model=UserModel, status_code=201)
def post_user(user_create: UserCreate, db: Session = Depends(get_db)) -> User:
    return storage.post_user(db, user_create.model_dump())


@user_router.delete("/{user_id}", status_code=204)
def delete_user(
    user: User = Depends(validate_user), db: Session = Depends(get_db)
) -> None:
    storage.delete_user(db, user)


@user_router.patch("/{user_id}", response_model=UserModel)
def patch_user(
    user_patch: UserPatch,
    user: User = Depends(validate_user),
    db: Session = Depends(get_db),
) -> User:
    return storage.patch_user(db, user, user_patch.model_dump(exclude_unset=True))


@user_router.get("/{user_id}/summary", response_model=SummaryModel)
def get_summary(user: User = Depends(validate_user), db: Session = Depends(get_db)):
    return storage.get_user_summary(db, user)
