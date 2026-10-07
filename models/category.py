from pydantic import BaseModel, ConfigDict
from typing import Optional

class CategoryPatch(BaseModel):
    name: Optional[str] = None

class CategoryCreate(BaseModel):
    name: str

class CategoryModel(CategoryCreate):
    model_config: ConfigDict = ConfigDict(from_attributes=True)

    id: int
    user_id: int