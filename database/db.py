from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker
from database.models import Base
from typing import Generator

engine: Engine = create_engine("sqlite:///database/expenses.db")
SessionLocal = sessionmaker(bind=engine)

def initialize_db() -> None:
    Base.metadata.create_all(bind=engine)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try: yield db
    finally: db.close()