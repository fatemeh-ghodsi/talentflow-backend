from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import profile_repository

from app.utils.file_manager import (
    save_file,
    delete_file,
)

from app.exceptions import (
    NotFoundError,
)

from app.core.logger import logger

from fastapi import UploadFile


class FileService:

    def __init__(self,db: AsyncSession, ):
        self.db = db

    async def upload_profile_photo(self,user_id: int,file: UploadFile,) -> str:

        profile = await profile_repository.get_by_user_id(user_id,self.db, )

        if profile is None:
            raise NotFoundError("Profile not found")

        if profile.photo_url:
            delete_file(profile.photo_url)

        photo_path = save_file(file)

        await profile_repository.update_profile(profile,self.db,
            { "photo_url": photo_path,},
        )

        logger.info(  f"Profile photo uploaded. user_id={user_id}")

        return photo_path

    async def upload_resume(self,user_id: int,file: UploadFile, ) -> str:

        profile = await profile_repository.get_by_user_id( user_id, self.db,)

        if profile is None:
            raise NotFoundError("Profile not found")

        if profile.resume_url:
            delete_file(profile.resume_url)

        resume_path = save_file(file)

        await profile_repository.update_profile( profile, self.db,
            {"resume_url": resume_path,},
        )

        logger.info(f"Resume uploaded. user_id={user_id}")

        return resume_path
    
    #============delete_profile_photo===================

    async def delete_profile_photo(self,user_id: int,) -> None:

        profile = await profile_repository.get_by_user_id(user_id,self.db, )

        if profile is None:
            raise NotFoundError("Profile not found")

        if profile.photo_url:
            delete_file(profile.photo_url)

            await profile_repository.update_profile(profile,self.db,
                {"photo_url": None,},
            )

        logger.info( f"Profile photo deleted. user_id={user_id}")
        
    #===============delete_resume=======================

    async def delete_resume( self,user_id: int,) -> None:

        profile = await profile_repository.get_by_user_id( user_id, self.db,)

        if profile is None:
            raise NotFoundError("Profile not found")

        if profile.resume_url:
            delete_file(profile.resume_url)

            await profile_repository.update_profile(profile, self.db,
                {"resume_url": None, },
            )

        logger.info(  f"Resume deleted. user_id={user_id}")