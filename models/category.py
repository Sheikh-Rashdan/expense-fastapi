from pydantic import BaseModel, ConfigDict

class CategoryPatch(BaseModel):
    name: str | None = None

class CategoryCreate(BaseModel):
    name: str

class CategoryModel(CategoryCreate):
    model_config: ConfigDict = ConfigDict(from_attributes=True)

    id: int
    user_id: int