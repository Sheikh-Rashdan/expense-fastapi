from pydantic import BaseModel, ConfigDict


class UserPatch(BaseModel):
    name: str | None = None
    email: str | None = None


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserModel(BaseModel):
    model_config: ConfigDict = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
