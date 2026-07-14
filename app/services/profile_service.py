from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import logger

from app.exceptions import (
    ConflictError,
    NotFoundError,
)

from app.models.profile import Profile

from app.repositories import (
    profile_repository,
    user_repository,
)

from app.schemas.profile import (
    CreateProfile,
    UpdateProfile,
)


class ProfileService:

    def __init__(self,  db: AsyncSession,):
        self.db = db


    # ====================create_profile=================================

    async def create_profile(
        self,
        user_id: int,
        profile_data: CreateProfile,
    ) -> Profile:

        user = await user_repository.get_by_id(user_id,self.db,  )

        if user is None:
            raise NotFoundError("User not found")

        existing = await profile_repository.get_by_user_id( user_id,self.db, )

        if existing is not None:
            raise ConflictError("Profile already exists")

        profile = Profile(
            user_id=user_id,
            bio=profile_data.bio,
            major=profile_data.major,
        )

        created = await profile_repository.create_profile(  profile, self.db,)

        logger.info( f"Profile created. user_id={user_id}")

        return created


    # ====================get_profile=================================

    async def get_profile(
        self,
        user_id: int,
    ) -> Profile:

        profile = await profile_repository.get_by_user_id(user_id,  self.db,)

        if profile is None:

            logger.warning( f"Profile not found. user_id={user_id}" )

            raise NotFoundError("Profile not found")

        return profile
    
    #======================get_profile_by_user_id================

    async def get_profile_by_user_id(
        self,
        user_id: int,
    ) -> Profile:

        profile = await profile_repository.get_by_user_id(user_id, self.db,)

        if profile is None:

            logger.warning(f"Profile not found. user_id={user_id}" )

            raise NotFoundError("Profile not found" )

        return profile

    
    # =====================update_profile==========================

    async def update_profile(
        self,
        user_id: int,
        profile_data: UpdateProfile,
    ) -> Profile:

        profile = await self.get_profile(user_id, )

        update_data = profile_data.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )

        if not update_data:
            return profile

        updated = await profile_repository.update_profile(
            profile,
            self.db,
            update_data,
        )

        logger.info(f"Profile updated. user_id={user_id}")

        return updated


    # ======================delete_profile===============================

    async def delete_profile( self,user_id: int,) -> None:

        profile = await self.get_profile(user_id,)

        await profile_repository.delete_profile( profile,self.db,)

        logger.info( f"Profile deleted. user_id={user_id}")