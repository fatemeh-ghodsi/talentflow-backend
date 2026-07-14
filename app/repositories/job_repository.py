from typing import Any

from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.pagination import Pagination

from app.models.jobs import Job

from app.schemas.job import JobFilter




# ========================== Get By Id================================

async def get_by_id( job_id: int,db: AsyncSession,) -> Job | None:

    result = await db.execute( select(Job).where(Job.id == job_id))

    return result.scalar_one_or_none()


# Company Jobs (Search + Filter + Pagination)
# ==========================================================

async def get_company_jobs(
    company_id: int,
    offset: int,
    limit: int,
    filters: JobFilter,
    db: AsyncSession,
) -> tuple[list[Job], int]:

    query = (select(Job).where(Job.company_id == company_id))

    count_query = (select(func.count()) .select_from(Job) .where(Job.company_id == company_id))

    # ---------------- Search ----------------

    if filters.search:

        query = query.where( Job.title.ilike(f"%{filters.search}%"))

        count_query = count_query.where(Job.title.ilike(f"%{filters.search}%") )

    # ---------------- Filters ----------------

    if filters.location:

        query = query.where( Job.location == filters.location)

        count_query = count_query.where( Job.location == filters.location)

    if filters.work_mode:

        query = query.where( Job.work_mode == filters.work_mode )

        count_query = count_query.where(Job.work_mode == filters.work_mode )

    if filters.employment_type:

        query = query.where( Job.employment_type == filters.employment_type )

        count_query = count_query.where(Job.employment_type == filters.employment_type )

    if filters.experience_level:

        query = query.where(  Job.experience_level == filters.experience_level )

        count_query = count_query.where(Job.experience_level == filters.experience_level )

    if filters.is_active is not None:

        query = query.where(  Job.is_active == filters.is_active)

        count_query = count_query.where(Job.is_active == filters.is_active)

    # ---------------- Sorting ----------------

    query = ( query.order_by(Job.created_at.desc()) .offset(offset) .limit(limit))
    jobs_result = await db.execute(query)

    jobs = jobs_result.scalars().all()

    total = await db.scalar(count_query)

    return list(jobs), total or 0



# =======================create_job===================================

async def create_job( job: Job, db: AsyncSession,) -> Job:

    try:

        db.add(job)

        await db.commit()

        await db.refresh(job)

        return job

    except SQLAlchemyError:

        await db.rollback()

        raise


# ============================update_job==============================

async def update_job(
    job: Job,
    db: AsyncSession,
    update_data: dict[str, Any],
) -> Job:

    try:

        for field, value in update_data.items():

            if hasattr(job, field):

                setattr(job, field, value)

        await db.commit()

        await db.refresh(job)

        return job

    except SQLAlchemyError:

        await db.rollback()

        raise


# =======================delete_job===================================

async def delete_job( job: Job,db: AsyncSession,) -> bool:

    try:

        await db.delete(job)

        await db.commit()

    except SQLAlchemyError:

        await db.rollback()

        raise 