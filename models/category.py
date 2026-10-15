from pydantic import BaseModel, ConfigDict, model_validator


class CategoryPatch(BaseModel):
    name: str | None = None

    @model_validator(mode="after")
    def validate_non_nullable_fields(self):
        fields = ("name",)
        for field in fields:
            if field in self.model_fields_set and getattr(self, field) is None:
                raise ValueError(f"{field} cannot be null")
        return self


class CategoryCreate(BaseModel):
    name: str


class CategoryModel(CategoryCreate):
    model_config: ConfigDict = ConfigDict(from_attributes=True)

    id: int
    user_id: int
