from sqlalchemy.ext.asyncio import AsyncSession

from app.common.pagination import Pagination
from app.common.responses import (
    PaginatedResponse,
    PaginationMetadata,
)

from app.core.logger import logger

from app.exceptions import (
    NotFoundError,
    ConflictError,
)

from app.models.user_skills import UserSkill

from app.repositories import user_skill_repository

from app.schemas.user_skill import (
    CreateUserSkill,
    UpdateUserSkill,
    UserSkillResponse,
)


class UserSkillService:

    def __init__( self,db: AsyncSession,):
        self.db = db


    # ========================create_user_skill=============================

    async def create_user_skill(
        self,
        user_id: int,
        user_skill_data: CreateUserSkill,
    ) -> UserSkill:

        existing = await user_skill_repository.get_one(
            user_id=user_id,
            skill_id=user_skill_data.skill_id,
            db=self.db,
        )

        if existing:
            raise ConflictError("Skill already exists." )

        user_skill = UserSkill(
            user_id=user_id,
            skill_id=user_skill_data.skill_id,
            level=user_skill_data.level,
        )

        created = await user_skill_repository.create_user_skill(self.db, user_skill, )

        logger.info( f"User skill created. " f"user_id={user_id}, skill_id={created.skill_id}")

        return created

    # ==================get_one=======================

    async def get_one(
        self,
        user_id: int,
        skill_id: int,
    ) -> UserSkill:

        user_skill = await user_skill_repository.get_one(
            user_id,
            skill_id,
            self.db,
        )

        if user_skill is None:
            raise NotFoundError("Skill not found." )

        return user_skill

    
    # =========================get_my_skills============================

    async def get_my_skills(
        self,
        user_id: int,
        pagination: Pagination,
    ) -> PaginatedResponse[UserSkillResponse]:

        user_skills, total = await user_skill_repository.get_my_skills(
            user_id=user_id,
            offset=pagination.offset,
            limit=pagination.limit,
            db=self.db,
        )

        metadata = PaginationMetadata(
            total_items=total,
            total_pages=(total + pagination.size - 1)
            // pagination.size,
            current_page=pagination.page,
            page_size=pagination.size,
        )

        return PaginatedResponse(
            items=user_skills,
            metadata=metadata,
        )
        
    #================get_user_skills=================
        
    async def get_user_skills(
    self,
    user_id: int,
    pagination: Pagination,
) -> PaginatedResponse[UserSkillResponse]:
        
        user_skills, total = await user_skill_repository.get_user_skills(
        user_id=user_id,
        offset=pagination.offset,
        limit=pagination.limit,
        db=self.db,
    )
        
        metadata = PaginationMetadata(
        total_items=total,
        total_pages=(total + pagination.size - 1) // pagination.size,
        current_page=pagination.page,
        page_size=pagination.size,
    )
        return PaginatedResponse(
        items=user_skills,
        metadata=metadata,
    )

    # ===================update_user_skill==========================

    async def update_user_skill(
        self,
        user_id: int,
        skill_id: int,
        user_skill_data: UpdateUserSkill,
    ) -> UserSkill:

        user_skill = await user_skill_repository.get_one(
            user_id,
            skill_id,
            self.db,
        )

        if user_skill is None:
            raise NotFoundError("Skill not found." )

        update_data = user_skill_data.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )

        if not update_data:
            return user_skill

        updated = await user_skill_repository.update_user_skill(
            self.db,
            user_skill,
            update_data,
        )

        logger.info( f"User skill updated. " f"user_id={user_id}, skill_id={skill_id}" )

        return updated

    
    # ====================delete_user_skill===============================

    async def delete_user_skill(
        self,
        user_id: int,
        skill_id: int,
    ) -> None:

        user_skill = await user_skill_repository.get_one(
            user_id,
            skill_id,
            self.db,
        )

        if user_skill is None:
            raise NotFoundError("Skill not found.")

        await user_skill_repository.delete_user_skill(user_skill, self.db,)

        logger.info( f"User skill deleted. " f"user_id={user_id}, skill_id={skill_id}" )