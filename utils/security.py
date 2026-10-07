from datetime import UTC, datetime, timedelta

import bcrypt
from jose import jwt

SECRET_KEY = "SUPER_SECRET_KEY"  # TODO:  replace


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash.encode())


def create_access_token(user_id: int) -> str:
    payload = {"sub": str(user_id), "exp": datetime.now(UTC) + timedelta(minutes=30)}
    return jwt.encode(payload, SECRET_KEY)
