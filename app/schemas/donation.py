from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt


class DonationBase(BaseModel):
    full_amount: Optional[PositiveInt]
    comment: Optional[str]


class DonationCreate(DonationBase):
    full_amount: PositiveInt


class DonationDB(DonationCreate):
    id: int
    user_id: Optional[int]
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
