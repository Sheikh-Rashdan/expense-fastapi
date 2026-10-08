from pydantic import BaseModel, ConfigDict


class UserPatch(BaseModel):
    name: str | None = None
    email: str | None = None


class UserAdminPatch(BaseModel):
    is_admin: bool


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserModel(BaseModel):
    model_config: ConfigDict = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    is_admin: bool


class UserLogin(BaseModel):
    email: str
    password: str


class AccessToken(BaseModel):
    token: str
