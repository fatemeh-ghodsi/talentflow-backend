from typing import Any

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.experience import Experience



# ======================== Get One=============================

async def get_one( user_id: int, experience_id: int, db: AsyncSession,) -> Experience | None:

    result = await db.execute(
        select(Experience).where(
            Experience.id == experience_id,
            Experience.user_id == user_id,
        )
    )

    return result.scalar_one_or_none()



# =========================Get User Experiences===========================

async def get_user_experiences(
    user_id: int,
    offset: int,
    limit: int,
    db: AsyncSession,
) -> tuple[list[Experience], int]:

    query = (
        select(Experience)
        .where(Experience.user_id == user_id)
        .order_by(Experience.start_date.desc())
        .offset(offset)
        .limit(limit)
    )

    count_query = (
        select(func.count())
        .select_from(Experience)
        .where(Experience.user_id == user_id)
    )

    result = await db.execute(query)

    experiences = list(result.scalars().all())

    total = await db.scalar(count_query)

    return experiences, total or 0




# ========================create_experience=============================

async def create_experience( experience: Experience,db: AsyncSession,) -> Experience:

    try:
        db.add(experience)

        await db.commit()
        await db.refresh(experience)

        return experience

    except SQLAlchemyError:
        await db.rollback()
        raise


# =====================================================
# Update
# =====================================================

async def update_experience(
    experience: Experience,
    update_data: dict[str, Any],
    db: AsyncSession,) -> Experience:

    try:
        for field, value in update_data.items():
            if hasattr(experience, field):
                setattr(experience, field, value)

        await db.commit()
        await db.refresh(experience)

        return experience

    except SQLAlchemyError:
        await db.rollback()
        raise




# ========================delete_experience=============================

async def delete_experience(
    experience: Experience,
    db: AsyncSession,
) -> None:

    try:
        await db.delete(experience)

        await db.commit()

    except SQLAlchemyError:
        await db.rollback()
        raise