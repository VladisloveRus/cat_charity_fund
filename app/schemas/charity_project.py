from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt]

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt

    @validator('name')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Имя не может быть пустым!')
        return value

    @validator('description')
    def description_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Описание проекта не может быть пустым!')
        return value


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectUpdate(CharityProjectBase):
    pass
