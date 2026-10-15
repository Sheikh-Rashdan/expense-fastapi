import datetime

from pydantic import BaseModel, ConfigDict, model_validator


class ExpensePatch(BaseModel):
    amount: float | None = None
    description: str | None = None
    date: datetime.date | None = None
    category_id: int | None = None

    @model_validator(mode="after")
    def validate_non_nullable_fields(self):
        fields = ("amount", "date", "category_id")
        for field in fields:
            if field in self.model_fields_set and getattr(self, field) is None:
                raise ValueError(f"{field} cannot be null")
        return self


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
