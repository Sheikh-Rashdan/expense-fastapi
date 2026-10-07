import datetime

from pydantic import BaseModel, ConfigDict


class ExpensePatch(BaseModel):
    amount: float | None = None
    description: str | None = None
    date: datetime.date | None = None
    category_id: int | None = None


class ExpenseCreate(BaseModel):
    amount: float
    description: str | None = None
    category_id: int | None = None
    date: datetime.date | None = None


class ExpenseModel(ExpenseCreate):
    model_config: ConfigDict = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    date: datetime.date
