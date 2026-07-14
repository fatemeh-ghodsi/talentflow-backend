from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import require_candidate
from app.common.pagination import Pagination
from app.common.responses import PaginatedResponse
from app.core.database import get_db

from app.models.users import User
from app.schemas.education import (
    EducationResponse,
    CreateEducation,
    UpdateEducation,
)
from app.services.education import EducationService

router = APIRouter(prefix="/educations", tags=["Educations"],)



#create_education
# ======================================

@router.post( "",response_model=EducationResponse,status_code=status.HTTP_201_CREATED,)
async def create_education(
    education_data: CreateEducation,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_candidate),
):
    return await EducationService(db).create_education(
        current_user.id,
        education_data,
    )



# Get One (Current User)
# =====================================================

@router.get("/me/{education_id}", response_model=EducationResponse,)
async def get_one(
    education_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_candidate),
):
    return await EducationService(db).get_one(
        current_user.id,
        education_id,
    )



# Get User Educations (Public)
# =====================================================

@router.get( "/user/{user_id}", response_model=PaginatedResponse[EducationResponse],)
async def get_user_educations(
    user_id: int,
    pagination: Pagination = Depends(),
    db: AsyncSession = Depends(get_db),
):
    return await EducationService(db).get_user_educations(
        user_id,
        pagination,
    )



# Update
# =====================================================

@router.put("/me/{education_id}",response_model=EducationResponse,)
async def update_education(
    education_id: int,
    update_data: UpdateEducation,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_candidate),
):
    return await EducationService(db).update_education(
        current_user.id,
        education_id,
        update_data,
    )



# delete_education
# =====================================================

@router.delete("/me/{education_id}",status_code=status.HTTP_204_NO_CONTENT,)

async def delete_education(
    education_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_candidate),
):
    await EducationService(db).delete_education(
        current_user.id,
        education_id,
    )