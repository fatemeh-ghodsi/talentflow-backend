from datetime import datetime, timezone

from sqlalchemy import delete, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.refresh_tokens import RefreshToken

#===================create===================
async def create(refresh_token: RefreshToken, db: AsyncSession,) -> RefreshToken:
    
    try:
        db.add(refresh_token)
        await db.commit()
        await db.refresh(refresh_token)
        return refresh_token

    except SQLAlchemyError:
        await db.rollback()
        raise

#====================get_by_hash=================

async def get_by_hash(
    token_hash: str,
    db: AsyncSession,
) -> RefreshToken | None:

    result = await db.execute(
        select(RefreshToken).where(
            RefreshToken.token_hash == token_hash
        )
    )

    return result.scalar_one_or_none()

#======================get_active_by_hash=================

async def get_active_by_hash(token_hash: str,  db: AsyncSession,) -> RefreshToken | None:

    result = await db.execute(
        select(RefreshToken).where(
            RefreshToken.token_hash == token_hash,
            RefreshToken.revoked_at.is_(None),
            RefreshToken.expires_at > datetime.now(timezone.utc),
        )
    )

    return result.scalar_one_or_none()

#=============================revoke=====================

async def revoke( refresh_token: RefreshToken, db: AsyncSession,) -> None:
    
    try:
        refresh_token.revoked_at = datetime.now(timezone.utc)

        await db.commit()
        await db.refresh(refresh_token)

    except SQLAlchemyError:
        await db.rollback()
        raise
    
    
#===================revoke_all_user_tokens===========

async def revoke_all_user_tokens( user_id: int,db: AsyncSession,) -> None:
    
    try:
        result = await db.execute(
            select(RefreshToken).where(
                RefreshToken.user_id == user_id,
                RefreshToken.revoked_at.is_(None),
            )
        )

        tokens = result.scalars().all()
        

        now = datetime.now(timezone.utc)

        for token in tokens:
            token.revoked_at = now

        await db.commit()

    except SQLAlchemyError:
        await db.rollback()
        raise

#=============delete_expired=================

async def delete_expired( db: AsyncSession,) -> None:
    
    try:
        await db.execute(
            delete(RefreshToken).where(
                RefreshToken.expires_at < datetime.now(timezone.utc)
            )
        )

        await db.commit()

    except SQLAlchemyError:
        await db.rollback()
        raise

#=================delete_old_revoked============

async def delete_old_revoked( before: datetime,db: AsyncSession,) -> None:
    
    try:
        await db.execute(
            delete(RefreshToken).where(
                RefreshToken.revoked_at.is_not(None),
                RefreshToken.revoked_at < before,
            )
        )

        await db.commit()

    except SQLAlchemyError:
        await db.rollback()
        raise