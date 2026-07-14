from typing import Any

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enum import ApplicationStatus
from app.models.applications import Application

#======================get_by_id===============

async def get_by_id(app_id: int,db: AsyncSession,) -> Application | None:

    result = await db.execute(
        select(Application).where(Application.id == app_id) )

    return result.scalar_one_or_none()


async def get_by_user_and_job( user_id: int, job_id: int,  db: AsyncSession,) -> Application | None:

    result = await db.execute(
        select(Application).where(
            Application.user_id == user_id,
            Application.job_id == job_id,
        )
    )

    return result.scalar_one_or_none()

#=================get_by_job_id===================
async def get_by_job_id(
    job_id: int,
    db: AsyncSession,
    offset: int = 0,
    limit: int = 10,
    status: ApplicationStatus | None = None,
) -> list[Application]:

    query = select(Application).where( Application.job_id == job_id )

    if status is not None:
        query = query.where( Application.status == status)

    query = (
        query
        .order_by(Application.created_at.desc())
        .offset(offset)
        .limit(limit)
    )

    result = await db.execute(query)

    return list(result.scalars().all())

#==================count_by_job_id================
async def count_by_job_id(
    job_id: int,
    db: AsyncSession,
    status: ApplicationStatus | None = None,
) -> int:

    query = (
        select(func.count())
        .select_from(Application)
        .where(Application.job_id == job_id)
    )

    if status is not None:
        query = query.where( Application.status == status)

    result = await db.execute(query)

    return result.scalar_one()

#==========================create_application====================
async def create_application( db: AsyncSession, application: Application,) -> Application:

    try:
        db.add(application)

        await db.commit()
        await db.refresh(application)

        return application

    except SQLAlchemyError:
        await db.rollback()
        raise

#=======================update_application====================
async def update_application(
    db: AsyncSession,
    application: Application,
    update_data: dict[str, Any],
) -> Application:

    try:

        for field, value in update_data.items():
            if hasattr(application, field):
                setattr(application, field, value)

        await db.commit()
        await db.refresh(application)

        return application

    except SQLAlchemyError:
        await db.rollback()
        raise

#==========================delete_application===================
async def delete_application( application: Application, db: AsyncSession,) -> None:

    try:

        await db.delete(application)

        await db.commit()

    except SQLAlchemyError:
        await db.rollback()
        raise