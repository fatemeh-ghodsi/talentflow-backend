from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.skills import Skill

#=============get_by_id=================

async def get_by_id(skill_id: int, db: AsyncSession,) -> Skill | None:

    result = await db.execute( select(Skill).where(Skill.id == skill_id ))

    return result.scalar_one_or_none()

#=======================get_by_name===============
async def get_by_name(name: str,db: AsyncSession,) -> Skill | None:

    result = await db.execute(select(Skill).where(Skill.name == name))

    return result.scalar_one_or_none()

#===============search_skills===============

async def search_skills(
    search: str,
    offset: int,
    limit: int,
    db: AsyncSession,
) -> tuple[list[Skill], int]:

    query = select(Skill)

    count_query = (
        select(func.count())
        .select_from(Skill)
    )

    if search:
        query = query.where(
            Skill.name.ilike(f"%{search}%")
        )

        count_query = count_query.where(
            Skill.name.ilike(f"%{search}%")
        )

    query = (
        query
        .order_by(Skill.name.asc())
        .offset(offset)
        .limit(limit)
    )

    result = await db.execute(query)

    skills = result.scalars().all()

    total = await db.scalar(count_query)

    return list(skills), total or 0