from typing import Any

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.education import Education



# =============================# Get One ========================

async def get_one(user_id: int,education_id: int,  db: AsyncSession,) -> Education | None:

    result = await db.execute(
        select(Education).where(Education.id == education_id,Education.user_id == user_id,   ))

    return result.scalar_one_or_none()




# ==========================Get User Educations===========================

async def get_user_educations(
    user_id: int,
    offset: int,
    limit: int,
    db: AsyncSession,
) -> tuple[list[Education], int]:

    query = (
        select(Education)
        .where(Education.user_id == user_id)
        .order_by(Education.start_date.desc())
        .offset(offset)
        .limit(limit)
    )

    count_query = (
        select(func.count())
        .select_from(Education)
        .where(Education.user_id == user_id)
    )

    result = await db.execute(query)

    educations = list(result.scalars().all())

    total = await db.scalar(count_query)

    return educations, total or 0




# =======================create_education==============================

async def create_education(
    education: Education,
    db: AsyncSession,
) -> Education:

    try:
        db.add(education)

        await db.commit()
        await db.refresh(education)

        return education

    except SQLAlchemyError:
        await db.rollback()
        raise


 
# ========================update_education=============================

async def update_education(
    education: Education,
    db: AsyncSession,
    update_data: dict[str, Any],
) -> Education:

    try:
        for field, value in update_data.items():
            if hasattr(education, field):
                setattr(education, field, value)

        await db.commit()
        await db.refresh(education)

        return education

    except SQLAlchemyError:
        await db.rollback()
        raise




# ========================== delete_education===========================

async def delete_education(
    education: Education,
    db: AsyncSession,
) -> None:

    try:
        await db.delete(education)

        await db.commit()

    except SQLAlchemyError:
        await db.rollback()
        raise 
    