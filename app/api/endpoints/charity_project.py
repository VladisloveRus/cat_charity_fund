from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import (
    create_charity_project as create,
    get_project_id_by_name,
    read_all_projects_from_db,
    update_charity_project as update,
    get_project_by_id,
    delete_charity_project as delete,
    start_investment_by_project,
)
from app.schemas import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.models import CharityProject

router = APIRouter(prefix='/charity_project', tags=['charity_project'])


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(charity_project.name, session)
    new_project = await create(charity_project, session)
    await start_investment_by_project(new_project, session)
    await session.refresh(new_project)
    return new_project


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    all_projects = await read_all_projects_from_db(session)
    return all_projects


@router.patch(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    charity_project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )

    if charity_project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!',
        )

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    
    if obj_in.full_amount is not None:
        if charity_project.invested_amount > obj_in.full_amount:
            raise HTTPException(
                status_code=400,
                detail='При редактировании проекта должно быть запрещено устанавливать требуемую сумму меньше внесённой!',
            )
    charity_project_result = await update(charity_project, obj_in, session)
    return charity_project_result


@router.delete(
    '/{charity_project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    charity_project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_project_exists(
        charity_project_id, session
    )
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!',
        )
    charity_project = await delete(charity_project, session)
    return charity_project


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    project_id = await get_project_id_by_name(project_name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!',
        )


async def check_charity_project_exists(
    charity_project_id: int,
    session: AsyncSession,
) -> CharityProject:
    charity_project = await get_project_by_id(charity_project_id, session)
    if charity_project is None:
        raise HTTPException(status_code=404, detail='Проект не найден!')
    return charity_project
