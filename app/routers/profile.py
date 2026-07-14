from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_active_user
from app.core.database import get_db
from app.models.users import User
from app.schemas.profile import CreateProfile, UpdateProfile, ProfileResponse
from app.services.profile_service import ProfileService
from app.services.file_service import FileService

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.post("", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(
    profile_data: CreateProfile,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return await ProfileService(db).create_profile(current_user.id, profile_data)

@router.get("/me", response_model=ProfileResponse)
async def get_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return await ProfileService(db).get_profile(current_user.id)

@router.get("/{user_id}", response_model=ProfileResponse)
async def get_profile_by_user_id(
    user_id: int, 
    db: AsyncSession = Depends(get_db)
):
    return await ProfileService(db).get_profile_by_user_id(user_id)

@router.put("", response_model=ProfileResponse)
async def update_profile(
    profile_data: UpdateProfile,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return await ProfileService(db).update_profile(current_user.id, profile_data)

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    await ProfileService(db).delete_profile(current_user.id)

@router.post("/photo")
async def upload_profile_photo(
    photo: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return await FileService(db).upload_profile_photo(current_user.id, photo)

@router.delete("/photo", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile_photo(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    await FileService(db).delete_profile_photo(current_user.id)

@router.post("/resume")
async def upload_resume(
    resume: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return await FileService(db).upload_resume(current_user.id, resume)

@router.delete("/resume", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    await FileService(db).delete_resume(current_user.id)
