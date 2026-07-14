from fastapi import (
    APIRouter,
    Depends,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import require_company

from app.common.pagination import Pagination

from app.common.responses import PaginatedResponse

from app.core.database import get_db

from app.models.users import User

from app.schemas.job import (
    CreateJob,
    UpdateJob,
    JobResponse,
    JobFilter,
)

from app.services.job import JobService


router = APIRouter(prefix="/jobs", tags=["Jobs"],)


# ========================create_job==================================

@router.post("",response_model=JobResponse,status_code=status.HTTP_201_CREATED,)
async def create_job(
    job_data: CreateJob,
    current_user: User = Depends(require_company),
    db: AsyncSession = Depends(get_db),
):
    service = JobService(db)

    return await service.create_job(current_user.id,job_data,)


# Company Jobs (must be before /{job_id})
# ==========================================================

@router.get("/me",response_model=PaginatedResponse[JobResponse],)

async def get_company_jobs(
    pagination: Pagination = Depends(),
    filters: JobFilter = Depends(),
    current_user: User = Depends(require_company),
    db: AsyncSession = Depends(get_db),
):
    service = JobService(db)

    return await service.get_company_jobs(
        current_user.id,
        pagination,
        filters,
    )



# ======================Get Single Job====================================

@router.get("/{job_id}",response_model=JobResponse,)

async def get_job( job_id: int, db: AsyncSession = Depends(get_db),):
    service = JobService(db)

    return await service.get_by_id(job_id)




# ===========================update_job===============================

@router.put("/{job_id}", response_model=JobResponse,)

async def update_job(
    job_id: int,
    job_data: UpdateJob,
    current_user: User = Depends(require_company),
    db: AsyncSession = Depends(get_db),
):
    service = JobService(db)

    return await service.update_job(
        current_user.id,
        job_id,
        job_data,
    )



# ========================delete_job==================================

@router.delete( "/{job_id}",status_code=status.HTTP_204_NO_CONTENT,)
async def delete_job(
    job_id: int,
    current_user: User = Depends(require_company),
    db: AsyncSession = Depends(get_db),
):
    service = JobService(db)

    await service.delete_job(
        current_user.id,
        job_id,
    )