from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

import storage.user as storage
from database.db import get_db
from database.models import User
from models.summary import SummaryModel
from models.user import AccessToken, UserCreate, UserLogin, UserModel, UserPatch
from utils.security import create_access_token, hash_password, verify_password

user_router = APIRouter(prefix="/users", tags=["user"])


def validate_user(user_id: int, db: Session = Depends(get_db)) -> User:
    user: User = storage.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def validate_login(user_login: UserLogin, db: Session = Depends(get_db)) -> User:
    user: User | None = storage.get_user_with_email(db, user_login.email)

    if user is not None:
        login_success = verify_password(user_login.password, user.password_hash)
        if login_success:
            return user

    raise HTTPException(status_code=401, detail="Incorrect email or password")


@user_router.post("/login", response_model=AccessToken)
def login_user(user: User = Depends(validate_login)) -> AccessToken:
    return {"token": create_access_token(user.id)}


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
    create_dict = user_create.model_dump()
    password: str = create_dict.pop("password")
    create_dict["password_hash"] = hash_password(password)

    return storage.post_user(db, create_dict)


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
