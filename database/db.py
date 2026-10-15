from collections.abc import Generator
from os import environ

from dotenv import load_dotenv
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from database.models import Base

load_dotenv()
DATABASE_URL = environ.get("DATABASE_URL")
if DATABASE_URL is None:
    raise ValueError(".env does not include `DATABASE_URL`")

engine: Engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def initialize_db() -> None:
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
