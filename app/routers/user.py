from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.auth.dependencies import get_current_active_user
from app.models.users import User
from app.schemas.user import UserOut, UserUpdate
from app.services.user import UserService


router = APIRouter( prefix="/users",tags=["Users"],)



# Get Current User
# =====================================================

@router.get("/me", response_model=UserOut)
async def get_me(
    current_user: User = Depends(get_current_active_user),
):
    return current_user


# Update Current User
# =====================================================

@router.patch("/me", response_model=UserOut)
async def update_me(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    service = UserService(db)
    return await service.update_user(current_user.id, user_data)



# Delete Current User
# =====================================================

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_me(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    service = UserService(db)
    await service.delete_user(current_user.id)
    return None
