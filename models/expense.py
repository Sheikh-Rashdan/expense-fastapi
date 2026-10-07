from pydantic import BaseModel, ConfigDict
import datetime
from typing import Optional

class ExpensePatch(BaseModel):
    amount: Optional[float] = None
    description: Optional[str] = None
    date: Optional[datetime.date] = None
    category_id: Optional[int] = None

class ExpenseCreate(BaseModel):
    amount: float
    description: Optional[str] = None
    category_id: Optional[int] = None

class ExpenseModel(ExpenseCreate):
    model_config: ConfigDict = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    date: datetime.date