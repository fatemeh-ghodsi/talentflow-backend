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

from app.models.jobs import Job

from app.repositories import (
    job_repository,
    user_repository,
)

from app.schemas.job import (
    CreateJob,
    UpdateJob,
    JobFilter,
    JobResponse,
)

from app.services.company import CompanyService


class JobService:

    def __init__( self,db: AsyncSession,):
        self.db = db

    
    
    # =====================Private==============================
    async def _verify_job_ownership(
        self,
        user_id: int,
        job_id: int,
    ) -> Job:

        job = await self.get_by_id(job_id)

        company = await CompanyService(
            self.db
        ).get_company(user_id)

        if job.company_id != company.id:

            logger.warning(
                f"Unauthorized job access. "
                f"user_id={user_id}, job_id={job_id}"
            )

            raise PermissionDenied(
                "You do not have permission to access this job."
            )

        return job

    # ========================get_by_id==========================

    async def get_by_id(
        self,
        job_id: int,
    ) -> Job:

        job = await job_repository.get_by_id(job_id, self.db,)

        if job is None:

            logger.warning(f"Job not found. job_id={job_id}")

            raise NotFoundError( "Job not found")

        return job

    # =====================get_company_jobs============================

    async def get_company_jobs(
        self,
        user_id: int,
        pagination: Pagination,
        filters: JobFilter,
    ) -> PaginatedResponse[JobResponse]:

        company = await CompanyService(
            self.db
        ).get_company(user_id)

        jobs, total = await job_repository.get_company_jobs(
            company_id=company.id,
            offset=pagination.offset,
            limit=pagination.limit,
            filters=filters,
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
            items=jobs,
            metadata=metadata,
        )

    # =======================create_job=====================

    async def create_job(
        self,
        user_id: int,
        job_data: CreateJob,
    ) -> Job:

        user = await user_repository.get_by_id(
            user_id,
            self.db,
        )

        if user is None:

            logger.warning( f"Create job failed. user_id={user_id}" )

            raise PermissionDenied("Not allowed to create job." )

        company = await CompanyService( self.db).get_company(user_id)

        job = Job(
            title=job_data.title,
            description=job_data.description,
            requirements=job_data.requirements,
            location=job_data.location,
            work_mode=job_data.work_mode,
            employment_type=job_data.employment_type,
            experience_level=job_data.experience_level,
            is_active=job_data.is_active,
            company_id=company.id,
        )

        created = await job_repository.create_job(job, self.db, )

        logger.info( f"Job created. company_id={company.id}" )

        return created

 
    # =====================update_job=====================================

    async def update_job(
        self,
        user_id: int,
        job_id: int,
        job_data: UpdateJob,
    ) -> Job:

        job = await self._verify_job_ownership(
            user_id,
            job_id,
        )

        update_data = job_data.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )

        if not update_data:
            return job

        updated = await job_repository.update_job(
            job,
            self.db,
            update_data,
        )

        logger.info( f"Job updated. job_id={job.id}")

        return updated

  
    # =====================delete_job============================

    async def delete_job(
        self,
        user_id: int,
        job_id: int,
    ) -> None:

        job = await self._verify_job_ownership(
            user_id,
            job_id,
        )

        await job_repository.delete_job(
            job,
            self.db,
        )

        logger.info(f"Job deleted. job_id={job.id}")