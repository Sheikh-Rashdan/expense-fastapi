from pydantic import BaseModel, ConfigDict
from typing import Optional

class UserPatch(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class UserCreate(BaseModel):
    name: str
    email: Optional[str] = None

class UserModel(UserCreate):
    model_config: ConfigDict = ConfigDict(from_attributes=True)

    id: int