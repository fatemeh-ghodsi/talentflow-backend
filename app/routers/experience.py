
from fastapi import (
    APIRouter,
    Depends,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import require_candidate

from app.common.pagination import Pagination
from app.common.responses import PaginatedResponse

from app.core.database import get_db

from app.models.users import User

from app.schemas.experience import (
    CreateExperience,
    UpdateExperience,
    ExperienceResponse,
)

from app.services.experience import ExperienceService


router = APIRouter( prefix="/experiences",tags=["Experiences"],)



# =====================create_experience================================

@router.post( "",response_model=ExperienceResponse,status_code=status.HTTP_201_CREATED,)

async def create_experience(
    experience_data: CreateExperience,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_candidate),):

    return await ExperienceService(db).create_experience(
        current_user.id,
        experience_data,)


# ==================== Get One (Current User)==========================

@router.get("/me/{experience_id}",response_model=ExperienceResponse,)

async def get_one(
    experience_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_candidate),
):

    return await ExperienceService(db).get_one(
        current_user.id,
        experience_id,
    )


# ==================# Get User Experiences (Public)===================

@router.get("/user/{user_id}", response_model=PaginatedResponse[ExperienceResponse],)
async def get_user_experiences(
    user_id: int,
    pagination: Pagination = Depends(),
    db: AsyncSession = Depends(get_db),
):

    return await ExperienceService(db).get_user_experiences( user_id,pagination,)


# ===================update_experience=============================

@router.put("/me/{experience_id}",response_model=ExperienceResponse,)
async def update_experience(
    experience_id: int,
    update_data: UpdateExperience,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_candidate),
):

    return await ExperienceService(db).update_experience(
        current_user.id,
        experience_id,
        update_data,
    )


# ====================delete_experience=================================

@router.delete("/me/{experience_id}", status_code=status.HTTP_204_NO_CONTENT,)
async def delete_experience(
    experience_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_candidate),
):

    await ExperienceService(db).delete_experience(
        current_user.id,
        experience_id,
    )
