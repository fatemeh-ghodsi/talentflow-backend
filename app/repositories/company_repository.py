from typing import Any

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.company import Company

#===================get_by_owner_id================

async def get_by_owner_id(owner_id: int,db: AsyncSession,) -> Company | None:

    result = await db.execute(
        select(Company).where(  Company.owner_id == owner_id ))

    return result.scalar_one_or_none()

#====================get_by_id======================
async def get_by_id(company_id: int, db: AsyncSession,) -> Company | None:

    result = await db.execute(select(Company).where(  Company.id == company_id))

    return result.scalar_one_or_none()

#======================create_company==================

async def create_company(company: Company,db: AsyncSession,) -> Company:

    try:
        db.add(company)

        await db.commit()
        await db.refresh(company)

        return company

    except SQLAlchemyError:
        await db.rollback()
        raise

#==================update_company===================
async def update_company(company: Company, db: AsyncSession,update_data: dict[str, Any],) -> Company:

    try:
        for field, value in update_data.items():
            if hasattr(company, field):
                setattr(company, field, value)

        await db.commit()
        await db.refresh(company)

        return company

    except SQLAlchemyError:
        await db.rollback()
        raise

#==========================delete_company====================
async def delete_company(
    company: Company,
    db: AsyncSession,
) -> None:

    try:
        await db.delete(company)

        await db.commit()

    except SQLAlchemyError:
        await db.rollback()
        raise