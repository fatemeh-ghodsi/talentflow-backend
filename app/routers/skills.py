from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

from app.common.pagination import Pagination
from app.common.responses import PaginatedResponse

from app.schemas.skill import SkillResponse

from app.services.skill import SkillService


router = APIRouter(prefix="/skills",tags=["Skills"],)




# =========================Get Skill By Id============================

@router.get("/{skill_id}",response_model=SkillResponse,)
async def get_by_id(
    skill_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = SkillService(db)

    return await service.get_by_id(
        skill_id,
    )



# =======================Search Skills (Autocomplete)==============================

@router.get( "", response_model=PaginatedResponse[SkillResponse],)
async def search_skills(
    search: str = "",
    pagination: Pagination = Depends(),
    db: AsyncSession = Depends(get_db),
):
    service = SkillService(db)

    return await service.search_skills(
        search=search,
        pagination=pagination,
    )