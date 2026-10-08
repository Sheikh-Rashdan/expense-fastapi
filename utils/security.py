from datetime import UTC, datetime, timedelta

import bcrypt
from fastapi import HTTPException
from jose import JWTError, jwt

SECRET_KEY = "SUPER_SECRET_KEY"  # TODO:  replace
ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash.encode())


def create_access_token(user_id: int) -> str:
    payload = {"sub": str(user_id), "exp": datetime.now(UTC) + timedelta(minutes=30)}
    return jwt.encode(payload, SECRET_KEY, ALGORITHM)


def decode_access_token(token: str) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])

        user_id: str = payload.get("sub")

        if user_id is None:
            raise ValueError("Invalid token")

        return int(user_id)

    except JWTError, ValueError:
        raise HTTPException(status_code=401, detail="Invalid token")
