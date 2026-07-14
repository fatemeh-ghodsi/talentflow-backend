from typing import Any

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_skills import UserSkill

#===============get_one=============

async def get_one( user_id: int,skill_id: int, db: AsyncSession,) -> UserSkill | None:

    result = await db.execute(
        select(UserSkill).where(
            UserSkill.user_id == user_id,
            UserSkill.skill_id == skill_id,
        )
    )

    return result.scalar_one_or_none()

#================get_my_skills============

async def get_my_skills(
    user_id: int,
    offset: int,
    limit: int,
    db: AsyncSession,
) -> tuple[list[UserSkill], int]:

    query = (
        select(UserSkill)
        .where(UserSkill.user_id == user_id)
        .order_by(UserSkill.learned_at.desc())
        .offset(offset)
        .limit(limit)
    )

    count_query = (
        select(func.count())
        .select_from(UserSkill)
        .where(UserSkill.user_id == user_id)
    )

    result = await db.execute(query)

    user_skills = list(result.scalars().all())

    total = await db.scalar(count_query)

    return user_skills, total or 0


#=================get_user_skills===============

async def get_user_skills(
    user_id: int,
    offset: int,
    limit: int,
    db: AsyncSession,
) -> tuple[list[UserSkill], int]:

    query = (
        select(UserSkill)
        .where(UserSkill.user_id == user_id)
        .order_by(UserSkill.learned_at.desc())
        .offset(offset)
        .limit(limit)
    )

    count_query = (
        select(func.count())
        .select_from(UserSkill)
        .where(UserSkill.user_id == user_id)
    )

    result = await db.execute(query)

    skills = list(result.scalars().all())

    total = await db.scalar(count_query)

    return skills, total or 0

#====================create_user_skill=================

async def create_user_skill(
    db: AsyncSession,
    user_skill: UserSkill,
) -> UserSkill:

    try:
        db.add(user_skill)

        await db.commit()
        await db.refresh(user_skill)

        return user_skill

    except SQLAlchemyError:
        await db.rollback()
        raise

#==============update_user_skill=============

async def update_user_skill(
    db: AsyncSession,
    user_skill: UserSkill,
    update_data: dict[str, Any],
) -> UserSkill:

    try:
        for field, value in update_data.items():
            if hasattr(user_skill, field):
                setattr(user_skill, field, value)

        await db.commit()
        await db.refresh(user_skill)

        return user_skill

    except SQLAlchemyError:
        await db.rollback()
        raise

#====================delete_user_skill=============

async def delete_user_skill(
    user_skill: UserSkill,
    db: AsyncSession,
) -> None:

    try:
        await db.delete(user_skill)

        await db.commit()

    except SQLAlchemyError:
        await db.rollback()
        raise