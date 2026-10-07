from pydantic import BaseModel, Field


class SummaryModel(BaseModel):
    total_expenses: float = Field(default=0, ge=0)
    expense_count: int = Field(default=0, ge=0)
    by_category: dict[str, float] = Field(default={})
