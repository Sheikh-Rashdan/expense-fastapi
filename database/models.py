from sqlalchemy import String, ForeignKey, Float, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime
from typing import Optional

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    categories: Mapped[list["Category"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    expenses: Mapped[list["Expense"]] = relationship(back_populates="user", cascade="all, delete-orphan")

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="categories")

    expenses: Mapped[list["Expense"]] = relationship(back_populates="category")

class Expense(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    date: Mapped[datetime.date] = mapped_column(Date, default=datetime.date.today, nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="expenses")

    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id", ondelete="SET NULL"), nullable=True)
    category: Mapped[Optional["Category"]] = relationship(back_populates="expenses")