from typing import Callable

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security import (
    oauth2_scheme,
    decode_access_token,
)

from app.core.database import get_db
from app.core.enum import UserRole
from app.core.logger import logger

from app.exceptions import (
    InvalidCredentials,
    PermissionDenied,
)

from app.models.users import User

from app.repositories import user_repository


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:

    payload = decode_access_token(token)

    user_id = payload.get("sub")

    if user_id is None:
        logger.warning("JWT does not contain subject.")
        raise InvalidCredentials("Invalid access token")

    user = await user_repository.get_by_id(
        int(user_id),
        db,
    )

    if user is None:
        logger.warning(
            f"User not found. id={user_id}"
        )
        raise InvalidCredentials("Invalid access token")

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:

   

    return current_user


def require_role(*roles: UserRole,) -> Callable:

    async def checker( current_user: User = Depends( get_current_active_user )) -> User:

        if current_user.role not in roles:

            logger.warning(  f"Permission denied. " f"user_id={current_user.id}")

            raise PermissionDenied("Permission denied" )

        return current_user

    return checker


require_admin = require_role(UserRole.ADMIN,)

require_company = require_role( UserRole.COMPANY,)

require_candidate = require_role(UserRole.CANDIDATE,)


