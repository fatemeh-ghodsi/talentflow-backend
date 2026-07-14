from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import require_admin
from app.common.pagination import Pagination
from app.common.responses import PaginatedResponse
from app.core.database import get_db
from app.schemas.user import UserOut
from app.services.admin_service import AdminService


router = APIRouter(prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(require_admin)],
)



# ========================Get All Users=============================

@router.get("/users", response_model=PaginatedResponse[UserOut])
async def get_all_users(
    pagination: Pagination = Depends(),
    db: AsyncSession = Depends(get_db),
):
    service = AdminService(db)
    return await service.get_all_users(pagination)
