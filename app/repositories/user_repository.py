from typing import Any, Dict

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.models.users import User


# ================== get_by_email ==================

async def get_by_email( email: str,db: AsyncSession,) -> User | None:

    result = await db.execute( select(User).where(User.email == email) )

    return result.scalar_one_or_none()


# ================== get_by_id ==================

async def get_by_id(user_id: int,db: AsyncSession,) -> User | None:

    result = await db.execute(
        select(User).where(
            User.id == user_id
        )
    )

    return result.scalar_one_or_none()


# ================== get_all_users ==================

async def get_all_users(
    offset: int,
    limit: int,
    db: AsyncSession,
) -> tuple[list[User], int]:

    result = await db.execute(
        select(User)
        .order_by(User.id.desc())
        .offset(offset)
        .limit(limit)
    )

    users = result.scalars().all()

    total = await db.scalar(select(func.count(User.id)))

    return users, total or 0


# ================== create ==================

async def create(
    user: User,
    db: AsyncSession,
) -> User:

    try:

        db.add(user)

        await db.commit()

        await db.refresh(user)

        return user

    except SQLAlchemyError:

        await db.rollback()

        raise


# ================== update_user ==================

async def update_user(
    user: User,
    db: AsyncSession,
    update_data: Dict[str, Any],
) -> User:

    try:

        for field, value in update_data.items():
            setattr(user, field, value)

        await db.commit()

        await db.refresh(user)

        return user

    except SQLAlchemyError:

        await db.rollback()

        raise


# ================== delete_user ==================

async def delete_user(user: User,db: AsyncSession,) -> bool:

    try:

        await db.delete(user)

        await db.commit()

        return True

    except SQLAlchemyError:

        await db.rollback()

        raise