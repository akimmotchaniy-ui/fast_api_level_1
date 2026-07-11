from pydantic import BaseModel, Field
from datetime import datetime


class BookCreateSchema(BaseModel):
    title: str = Field(examples=['Я, легенда'])
    author: str
    price: int = Field(ge=2)
    description: str = ''


class BookSavedSchema(BookCreateSchema):
    id: str = Field(examples=['6a512ade462303c800b8bead'])
    created_at: datetime