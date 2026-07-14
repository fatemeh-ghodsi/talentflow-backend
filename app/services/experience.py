
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.pagination import Pagination
from app.common.responses import (
    PaginatedResponse,
    PaginationMetadata,
)

from app.core.logger import logger

from app.exceptions import (
    NotFoundError,
    PermissionDenied,
)

from app.models.experience import Experience

from app.repositories import experience_repository

from app.schemas.experience import (
    CreateExperience,
    UpdateExperience,
    ExperienceResponse,
)


class ExperienceService:

    def __init__( self, db: AsyncSession, ):
        self.db = db

    
    # ========================Private=============================

    async def _verify_experience(
        self,
        user_id: int,
        experience_id: int,
    ) -> Experience:

        experience = await experience_repository.get_one(
            user_id=user_id,
            experience_id=experience_id,
            db=self.db,
        )

        if experience is None:
            logger.warning(
                f"Experience not found or access denied. "
                f"user_id={user_id}, experience_id={experience_id}"
            )

            raise PermissionDenied(
                "You do not have permission to access this experience."
            )

        return experience
    
    #=================create_experience==============

    async def create_experience(
        self,
        user_id: int,
        experience_data: CreateExperience,
    ) -> Experience:

        if experience_data.is_current:
            experience_data.end_date = None

        elif experience_data.end_date is None:
            raise ValueError(
                "End date is required when is_current is False."
            )

        experience = Experience(
            user_id=user_id,
            job_title=experience_data.job_title,
            company_name=experience_data.company_name,
            location=experience_data.location,
            start_date=experience_data.start_date,
            end_date=experience_data.end_date,
            is_current=experience_data.is_current,
            description=experience_data.description,
        )

        created = await experience_repository.create_experience(
            experience,
            self.db,
        )

        logger.info(
            f"Experience created. " f"user_id={user_id}, experience_id={created.id}" )

        return created

    # ==================== Get One=====================

    async def get_one(
        self,
        user_id: int,
        experience_id: int,
    ) -> Experience:

        experience = await experience_repository.get_one(
            user_id=user_id,
            experience_id=experience_id,
            db=self.db,
        )

        if experience is None:
            logger.warning(
                f"Experience not found. "
                f"user_id={user_id}, experience_id={experience_id}"
            )

            raise NotFoundError(
                "Experience not found."
            )

        return experience

    # ====================get_user_experiences=================================

    async def get_user_experiences(
        self,
        user_id: int,
        pagination: Pagination,
    ) -> PaginatedResponse[ExperienceResponse]:

        experiences, total = (
            await experience_repository.get_user_experiences(
                user_id=user_id,
                offset=pagination.offset,
                limit=pagination.limit,
                db=self.db,
            )
        )

        metadata = PaginationMetadata(
            total_items=total,
            total_pages=(total + pagination.size - 1) // pagination.size,
            current_page=pagination.page,
            page_size=pagination.size,
        )

        return PaginatedResponse(
            items=experiences,
            metadata=metadata,
        )

    
    # =====================update_experience================================

    async def update_experience(
        self,
        user_id: int,
        experience_id: int,
        experience_data: UpdateExperience,
    ) -> Experience:

        experience = await self._verify_experience(
            user_id,
            experience_id,
        )

        update_data = experience_data.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )

        if "is_current" in update_data:
            if update_data["is_current"]:
                update_data["end_date"] = None
            elif "end_date" not in update_data:
                raise ValueError(
                    "End date is required when is_current is False."
                )

        if not update_data:
            return experience

        updated = await experience_repository.update_experience(
            experience=experience,
            update_data=update_data,
            db=self.db,
        )

        logger.info(
            f"Experience updated. "f"user_id={user_id}, experience_id={experience_id}"  )

        return updated

    # =====================delete_experience================================

    async def delete_experience(
        self,
        user_id: int,
        experience_id: int,
    ) -> None:

        experience = await self._verify_experience(
            user_id,
            experience_id,
        )

        await experience_repository.delete_experience(
            experience,
            self.db,
        )

        logger.info(
            f"Experience deleted. " f"user_id={user_id}, experience_id={experience_id}" )
