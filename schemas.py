from pydantic import BaseModel, Field
from datetime import datetime


class TourCreateSchema(BaseModel):
    title: str = Field(examples=['Тур до Карпат'])
    country: str = Field(examples=['Україна'])
    city: str = Field(examples=['Буковель'])
    description: str = ''
    price: int = Field(ge=1, examples=[4500])
    duration_days: int = Field(ge=1, examples=[3])
    available_seats: int = Field(ge=0, examples=[12])


class TourUpdateSchema(BaseModel):
    """Усі поля необов'язкові — оновлюємо тільки те, що передали."""
    title: str | None = None
    country: str | None = None
    city: str | None = None
    description: str | None = None
    price: int | None = Field(default=None, ge=1)
    duration_days: int | None = Field(default=None, ge=1)
    available_seats: int | None = Field(default=None, ge=0)


class TourSavedSchema(TourCreateSchema):
    id: str = Field(examples=['6a512ade462303c800b8bead'])
    created_at: datetime
