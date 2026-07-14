from sqlalchemy.ext.asyncio import AsyncSession

from app.common.pagination import Pagination
from app.common.responses import (
    PaginatedResponse,
    PaginationMetadata,
)

from app.core.logger import logger

from app.exceptions import (
    NotFoundError,
)

from app.models.education import Education

from app.repositories import education_repository

from app.schemas.education import (
    CreateEducation,
    UpdateEducation,
    EducationResponse,
)


class EducationService:

    def __init__( self,db: AsyncSession,):
        self.db = db


    # ======================Private===============================

    async def verify_education(
        self,
        user_id: int,
        education_id: int,
    ) -> Education:

        education = await education_repository.get_one(
            user_id,
            education_id,
            self.db,
        )

        if education is None:
            raise NotFoundError("Education not found.")

        return education

    
    # =====================create_education=========================

    async def create_education(
        self,
        user_id: int,
        education_data: CreateEducation,
    ) -> Education:

        if education_data.is_current:
            education_data.end_date = None

        elif education_data.end_date is None:
            raise ValueError(
                "End date is required when is_current is False."
            )

        education = Education(
            user_id=user_id,
            institution=education_data.institution,
            field_of_study=education_data.field_of_study,
            degree=education_data.degree,
            start_date=education_data.start_date,
            end_date=education_data.end_date,
            is_current=education_data.is_current,
            description=education_data.description,
        )

        created = await education_repository.create_education(
            education,
            self.db,
        )

        logger.info(
            f"Education created. " f"user_id={user_id}, education_id={created.id}" )

        return created

    
    # ===================# Get One=========================

    async def get_one(
        self,
        user_id: int,
        education_id: int,
    ) -> Education:

        return await self.verify_education(
            user_id,
            education_id,
        )

    # ====================Get User Educations=================

    async def get_user_educations(
        self,
        user_id: int,
        pagination: Pagination,
    ) -> PaginatedResponse[EducationResponse]:

        educations, total = (
            await education_repository.get_user_educations(
                user_id=user_id,
                offset=pagination.offset,
                limit=pagination.limit,
                db=self.db,
            )
        )

        metadata = PaginationMetadata(
            total_items=total,
            total_pages=(total + pagination.size - 1)
            // pagination.size,
            current_page=pagination.page,
            page_size=pagination.size,
        )

        return PaginatedResponse(
            items=educations,
            metadata=metadata,
        )

    # =======================update_education==============================

    async def update_education(
        self,
        user_id: int,
        education_id: int,
        update_data: UpdateEducation,
    ) -> Education:

        education = await self.verify_education(
            user_id,
            education_id,
        )

        update_values = update_data.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )

        if "is_current" in update_values:

            if update_values["is_current"]:
                update_values["end_date"] = None

            elif "end_date" not in update_values:
                raise ValueError(
                    "End date is required when is_current is False."
                )

        if not update_values:
            return education

        updated = await education_repository.update_education(
            education,
            self.db,
            update_values,
        )

        logger.info(
            f"Education updated. " f"user_id={user_id}, education_id={education_id}")

        return updated

    
    # =========================Delete============================

    async def delete_education(
        self,
        user_id: int,
        education_id: int,
    ) -> None:

        education = await self.verify_education(
            user_id,
            education_id,
        )

        await education_repository.delete_education(
            education,
            self.db, )

        logger.info(
            f"Education deleted. "f"user_id={user_id}, education_id={education_id}"  )