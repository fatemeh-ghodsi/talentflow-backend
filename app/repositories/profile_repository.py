from typing import Any

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.profile import Profile

#======================get_by_user_id==================

async def get_by_user_id(user_id: int, db: AsyncSession,) -> Profile | None:

    result = await db.execute(
        select(Profile).where(
            Profile.user_id == user_id
        )
    )

    return result.scalar_one_or_none()

#=================create_profile=======================

async def create_profile(
    profile: Profile,
    db: AsyncSession,
) -> Profile:

    try:
        db.add(profile)

        await db.commit()
        await db.refresh(profile)

        return profile

    except SQLAlchemyError:
        await db.rollback()
        raise

#==================update_profile===================
async def update_profile(
    profile: Profile,
    db: AsyncSession,
    update_data: dict[str, Any],
) -> Profile:

    try:
        for field, value in update_data.items():
            if hasattr(profile, field):
                setattr(profile, field, value)

        await db.commit()
        await db.refresh(profile)

        return profile

    except SQLAlchemyError:
        await db.rollback()
        raise

#============================delete_profile====================
async def delete_profile(
    profile: Profile,
    db: AsyncSession,
) -> None:

    try:
        await db.delete(profile)

        await db.commit()

    except SQLAlchemyError:
        await db.rollback()
        raise