from pydantic import BaseModel, ConfigDict, model_validator


class UserPatch(BaseModel):
    name: str | None = None
    email: str | None = None

    @model_validator(mode="after")
    def validate_non_nullable_fields(self):
        fields = ("name", "email")
        for field in fields:
            if field in self.model_fields_set and getattr(self, field) is None:
                raise ValueError(f"{field} cannot be null")
        return self


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
