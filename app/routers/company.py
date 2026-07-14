from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import require_company
from app.core.database import get_db

from app.models.users import User

from app.schemas.company import (
    CompanyResponse,
    CreateCompany,
    UpdateCompany,
)

from app.services.company import CompanyService


router = APIRouter(prefix="/company",tags=["company"],)

#================create_company================

@router.post("/me",response_model=CompanyResponse,status_code=status.HTTP_201_CREATED,)
async def create_company(
    company_data: CreateCompany,
    current_user: User = Depends(require_company),
    db: AsyncSession = Depends(get_db),
):
    service = CompanyService(db)

    return await service.create_company(
        current_user.id,
        company_data,
    )


#======================get_company===================

@router.get( "/me",response_model=CompanyResponse,)
async def get_company(current_user: User = Depends(require_company),
                    db: AsyncSession = Depends(get_db),):
    
    service = CompanyService(db)

    return await service.get_company(current_user.id, )


#==================update_company================

@router.put("/me", response_model=CompanyResponse,)
async def update_company(
    company_data: UpdateCompany,
    current_user: User = Depends(require_company),
    db: AsyncSession = Depends(get_db),
):
    service = CompanyService(db)

    return await service.update_company(
        current_user.id,
        company_data,
    )

#=====================delete_company================

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT,)
async def delete_company(
    current_user: User = Depends(require_company),
    db: AsyncSession = Depends(get_db),
):
    service = CompanyService(db)

    await service.delete_company(current_user.id)
    
    