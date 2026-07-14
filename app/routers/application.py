from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import (
    require_candidate,
    require_company,
)
from app.common.pagination import Pagination

from app.common.responses import PaginatedResponse

from app.core.database import get_db

from app.models.users import User

from app.core.enum import ApplicationStatus

from app.schemas.application import (
    ApplicationResponse,
    UpdateApplicationStatus,
)

from app.services.application import ApplicationService


router = APIRouter( prefix="/applications",tags=["Applications"],)



# ======================================================
# Candidate
# ======================================================

#--------create_application----------------

@router.post("",response_model=ApplicationResponse,status_code=status.HTTP_201_CREATED,)

async def create_application(
    job_id: int,
    current_user: User = Depends(require_candidate),
    db: AsyncSession = Depends(get_db),):
    
    service = ApplicationService(db)

    return await service.create_application(current_user.id, job_id,)


#---------------get_my_application------------

@router.get("/me/{app_id}",response_model=ApplicationResponse,)

async def get_my_application(
    app_id: int,
    current_user: User = Depends(require_candidate),
    db: AsyncSession = Depends(get_db),
):
    service = ApplicationService(db)

    return await service.get_my_application(current_user.id,  app_id,)

#---------------delete_application-------------

@router.delete("/me/{app_id}",status_code=status.HTTP_204_NO_CONTENT,)

async def delete_application(
    app_id: int,
    current_user: User = Depends(require_candidate),
    db: AsyncSession = Depends(get_db),
):
    service = ApplicationService(db)

    await service.delete_application( current_user.id, app_id,)


# ======================================================
# Company
# ======================================================

#---------------get_job_applications------------

@router.get("/jobs/{job_id}", response_model=PaginatedResponse[ApplicationResponse],)

async def get_job_applications(
    job_id: int,
    pagination: Pagination = Depends(),
    status: ApplicationStatus | None = None,
    current_user: User = Depends(require_company),
    db: AsyncSession = Depends(get_db),
):
    service = ApplicationService(db)

    return await service.get_job_applications(
        current_user.id,
        job_id,
        pagination,
        status,
    )

#--------------update_application_status--------------

@router.put("/{app_id}/status",response_model=ApplicationResponse,)

async def update_application_status(
    app_id: int,
    application_data: UpdateApplicationStatus,
    current_user: User = Depends(require_company),
    db: AsyncSession = Depends(get_db),
):
    service = ApplicationService(db)

    return await service.update_application_status(
        current_user.id,
        app_id,
        application_data,)