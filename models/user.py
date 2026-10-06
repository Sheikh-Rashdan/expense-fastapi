from pydantic import BaseModel, ConfigDict

class UserPatch(BaseModel):
    name: str | None = None
    email: str | None = None

class UserCreate(BaseModel):
    name: str
    email: str | None = None

class UserModel(UserCreate):
    model_config: ConfigDict = ConfigDict(from_attributes=True)

    id: int