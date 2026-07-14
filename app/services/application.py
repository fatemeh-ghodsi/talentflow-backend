from math import ceil

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.pagination import Pagination
from app.common.responses import (
    PaginatedResponse,
    PaginationMetadata,
)

from app.core.enum import ApplicationStatus
from app.core.logger import logger

from app.exceptions import (
    ConflictError,
    NotFoundError,
    PermissionDenied,
    ValidationError,
)

from app.models.applications import Application

from app.repositories import application_repository

from app.schemas.application import (
    ApplicationResponse,
    UpdateApplicationStatus,
)

from app.services.company import CompanyService
from app.services.job import JobService


ALLOWED_TRANSITIONS = {
    ApplicationStatus.PENDING: [
        ApplicationStatus.ACCEPTED,
        ApplicationStatus.REJECTED,
        ApplicationStatus.WITHDRAWN,
    ],
}


class ApplicationService:

    def __init__(self, db: AsyncSession):
        self.db = db

    # Private
    # =====================================================

    async def _verify_company_job(
        self,
        user_id: int,
        job_id: int,
    ):
        company = await CompanyService(self.db).get_company(user_id)

        job = await JobService(self.db).get_by_id(job_id)

        if job.company_id != company.id:
            logger.warning(
                f"Unauthorized job access. "
                f"user_id={user_id}, job_id={job_id}" )
            raise PermissionDenied("You do not have permission to access this job." )

        return job

    
    # Candidate
    # =====================================================
    
#=--------------create_application-------------------

    async def create_application(
        self,
        user_id: int,
        job_id: int,
    ) -> Application:

        await JobService(self.db).get_by_id(job_id)

        existing = await application_repository.get_by_user_and_job(
            user_id,
            job_id,
            self.db,
        )

        if existing:
            raise ConflictError(  "You have already applied for this job.")

        application = Application(
            user_id=user_id,
            job_id=job_id,
            status=ApplicationStatus.PENDING,
        )

        created = await application_repository.create_application(
            self.db,
            application,
        )

        logger.info(  f"Application created. "f"user_id={user_id}, job_id={job_id}")

        return created
    
#-----------------get_my_application----------------

    async def get_my_application(
        self,
        user_id: int,
        app_id: int,
    ) -> Application:

        app = await application_repository.get_by_id(
            app_id,
            self.db,
        )

        if app is None:
            raise NotFoundError("Application not found")

        if app.user_id != user_id:
            logger.warning(  f"Unauthorized application access. "  f"user_id={user_id}, app_id={app_id}" )
            raise PermissionDenied("You do not have permission to access this application."  )

        return app
#------------delete_application--------------

    async def delete_application(
        self,
        user_id: int,
        app_id: int,
    ) -> None:

        app = await self.get_my_application(user_id, app_id, )

        await application_repository.delete_application( app, self.db,)

        logger.info( f"Application deleted. "  f"user_id={user_id}, app_id={app_id}" )

    
    # Company
    # =====================================================

#-----------------get_job_applications---------------

    async def get_job_applications(
        self,
        user_id: int,
        job_id: int,
        pagination: Pagination,
        status: ApplicationStatus | None = None,
    ) -> PaginatedResponse[ApplicationResponse]:

        await self._verify_company_job(user_id, job_id,)

        applications = await application_repository.get_by_job_id(
            job_id=job_id,
            db=self.db,
            offset=pagination.offset,
            limit=pagination.limit,
            status=status,
        )

        total_items = await application_repository.count_by_job_id(
            job_id=job_id,
            db=self.db,
            status=status,
        )

        total_pages = ceil( total_items / pagination.size) if total_items else 1

        return PaginatedResponse(
            items=applications,
            metadata=PaginationMetadata(
                total_items=total_items,
                total_pages=total_pages,
                current_page=pagination.page,
                page_size=pagination.size,
            ),
        )
#----------------update_application_status--------------

    async def update_application_status(
        self,
        user_id: int,
        app_id: int,
        application_data: UpdateApplicationStatus,
    ) -> Application:

        app = await application_repository.get_by_id( app_id,  self.db,  )

        if app is None:
            raise NotFoundError("Application not found")

        await self._verify_company_job(  user_id, app.job_id, )

        update_data = application_data.model_dump(exclude_unset=True,exclude_none=True, )

        if not update_data:
            return app

        new_status = update_data["status"]

        allowed = ALLOWED_TRANSITIONS.get( app.status,  [],  )

        if new_status not in allowed:
            logger.warning(  f"Invalid transition. "f"{app.status} -> {new_status}"  )
            
            raise ValidationError( "Status transition is not allowed.")

        updated = await application_repository.update_application(self.db,app,  update_data,)

        logger.info( f"Application updated. "f"app_id={app.id}, status={new_status}"  )

        return updated