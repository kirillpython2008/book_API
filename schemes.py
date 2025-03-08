from pydantic import BaseModel, Field


class BookScheme(BaseModel):
    name: str = Field(max_length=32)


class DeleteBookScheme(BaseModel):
    id: int = Field(ge=1, le=1000000)


class EditBookScheme(BookScheme):
    id: int = Field(ge=1, le=1000000)
