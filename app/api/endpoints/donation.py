from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.crud import create_donation as create
from app.crud import (get_donation_by_user, read_all_donation_from_db,
                      start_investment_by_donation)
from app.models import User
from app.schemas import DonationCreate, DonationDB

router = APIRouter(prefix='/donation', tags=['donations'])


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
    response_model_exclude={
        'close_date',
        'fully_invested',
        'invested_amount',
        'user_id',
    },
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    new_donation = await create(donation, session, user)
    await start_investment_by_donation(new_donation, session)
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/',
    response_model=List[DonationDB],
    response_model_exclude_none=True,
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    return await read_all_donation_from_db(session)


@router.get(
    '/my',
    response_model=List[DonationDB],
    response_model_exclude_none=True,
    response_model_exclude={
        'close_date',
        'fully_invested',
        'invested_amount',
        'user_id',
    },
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    return await get_donation_by_user(session, user)
