from datetime import datetime
from typing import List, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import false

from app.models import CharityProject, Donation


async def start_investment_by_donation(
    donation: Donation, session: AsyncSession
):
    uninvested_projects = await session.execute(
        select(CharityProject)
        .where(CharityProject.fully_invested == False)
        .order_by(CharityProject.create_date)
    )
    uninvested_projects_list: List[
        CharityProject
    ] = uninvested_projects.scalars().all()
    for project in uninvested_projects_list:
        have_donation = donation.full_amount - donation.invested_amount
        if have_donation > 0:
            need_donation = project.full_amount - project.invested_amount
            if need_donation >= have_donation:
                project.invested_amount += have_donation
                donation.invested_amount += have_donation
            else:
                project.invested_amount += need_donation
                donation.invested_amount += need_donation
            if project.invested_amount == project.full_amount:
                project.fully_invested = True
                project.close_date = datetime.now()
            if donation.invested_amount == donation.full_amount:
                donation.fully_invested = True
                donation.close_date = datetime.now()
    await session.commit()
    return donation

async def start_investment_by_project(
    project: CharityProject, session: AsyncSession
):
    uninvested_donations = await session.execute(
        select(Donation)
        .where(Donation.fully_invested == False)
        .order_by(Donation.create_date)
    )
    uninvested_donations_list: List[
        Donation
    ] = uninvested_donations.scalars().all()
    for donation in uninvested_donations_list:
        need_donation = project.full_amount - project.invested_amount
        if need_donation > 0:
            have_donation = donation.full_amount - donation.invested_amount
            if need_donation >= have_donation:
                project.invested_amount += have_donation
                donation.invested_amount += have_donation
            else:
                project.invested_amount += need_donation
                donation.invested_amount += need_donation
            if project.invested_amount == project.full_amount:
                project.fully_invested = True
                project.close_date = datetime.now()
            if donation.invested_amount == donation.full_amount:
                donation.fully_invested = True
                donation.close_date = datetime.now()
    await session.commit()
    return project
