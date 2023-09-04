from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Donation, User
from app.schemas.donation import DonationCreate


async def create_donation(
    new_donation: DonationCreate,
    session: AsyncSession,
    user: User,
) -> Donation:
    new_donation_data = new_donation.dict()
    new_donation_data['user_id'] = user.id
    db_donation = Donation(**new_donation_data)
    session.add(db_donation)
    await session.commit()
    await session.refresh(db_donation)
    return db_donation


async def read_all_donation_from_db(
    session: AsyncSession,
) -> List[Donation]:
    db_donations = await session.execute(select(Donation))
    return db_donations.scalars().all()


async def get_donation_by_user(
    session: AsyncSession,
    user: User,
) -> List[Donation]:
    db_donations = await session.execute(
        select(Donation).where(Donation.user_id == user.id)
    )
    return db_donations.scalars().all()
