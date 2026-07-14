from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.schemas.user import (
    UserCreate,
    PasswordChangeRequest,
    UserOut,
)

from app.schemas.auth import (
    Token,
    RefreshTokenRequest,
)

from app.auth.dependencies import get_current_active_user

from app.models.users import User

from app.services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["Authentication"],)



# =====================Register================================

@router.post( "/register",response_model=UserOut, status_code=status.HTTP_201_CREATED,)

async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db),):
    
    service = AuthService(db)
    return await service.register(user_data)




# ========================Login=============================

@router.post("/login",response_model=Token,)

async def login(form_data: OAuth2PasswordRequestForm = Depends(),db: AsyncSession = Depends(get_db),):

    service = AuthService(db)
    
    return await service.login(form_data)


# ========================Refresh Token=============================

@router.post("/refresh",response_model=Token,)

async def refresh(
    refresh_request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),):
    
    service = AuthService(db)
    return await service.refresh(refresh_request)



# ============================ Logout=========================

@router.post("/logout",status_code=status.HTTP_204_NO_CONTENT,)

async def logout(
    refresh_request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    await service.logout(refresh_request.refresh_token)


# ====================Change Password=================================

@router.post("/change-password", status_code=status.HTTP_204_NO_CONTENT,)

async def change_password(
    password_data: PasswordChangeRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)

    await service.change_password( current_user.id,password_data,)