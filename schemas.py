from pydantic import BaseModel, Field
from datetime import datetime, date


class TourCreateSchema(BaseModel):
    title: str = Field(examples=['Тиждень у Барселоні'])
    country: str = Field(examples=['Іспанія'])
    price: int = Field(ge=1)
    duration_days: int = Field(ge=1, examples=[7])
    start_date: date = Field(examples=['2026-08-01'])
    description: str = ''


class TourUpdateSchema(BaseModel):
    title: str | None = None
    country: str | None = None
    price: int | None = Field(default=None, ge=1)
    duration_days: int | None = Field(default=None, ge=1)
    start_date: date | None = None
    description: str | None = None


class TourSavedSchema(TourCreateSchema):
    id: str = Field(examples=['6a512ade462303c800b8bead'])
    created_at: datetime
