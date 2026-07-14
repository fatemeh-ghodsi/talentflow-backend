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

from app.schemas.user_skill import (
    CreateUserSkill,
    UpdateUserSkill,
    UserSkillResponse,
)

from app.services.user_skill import UserSkillService


router = APIRouter(prefix="/user-skills",tags=["User Skills"],)



# =======================create_user_skill==============================

@router.post( "",response_model=UserSkillResponse,status_code=status.HTTP_201_CREATED,)

async def create_user_skill(
    user_skill_data: CreateUserSkill,
    current_user: User = Depends(require_candidate),
    db: AsyncSession = Depends(get_db),
):
    service = UserSkillService(db)

    return await service.create_user_skill(
        current_user.id,
        user_skill_data,
    )




# =========================get_one============================

@router.get( "/me/{skill_id}", response_model=UserSkillResponse,)

async def get_one(
    skill_id: int,
    current_user: User = Depends(require_candidate),
    db: AsyncSession = Depends(get_db),
):
    service = UserSkillService(db)

    return await service.get_one(
        current_user.id,
        skill_id,
    )

#==================get_user_skills==================

@router.get("/user/{user_id}", response_model=PaginatedResponse[UserSkillResponse],)

async def get_user_skills(
    user_id: int,
    pagination: Pagination = Depends(),
    db: AsyncSession = Depends(get_db),
):

    service = UserSkillService(db)

    return await service.get_user_skills(
        user_id,
        pagination,
    )

# ========================= Get My Skills============================

@router.get("/me",response_model=PaginatedResponse[UserSkillResponse],)
async def get_my_skills(
    pagination: Pagination = Depends(),
    current_user: User = Depends(require_candidate),
    db: AsyncSession = Depends(get_db),
):
    service = UserSkillService(db)

    return await service.get_my_skills(
        current_user.id,
        pagination,
    )




# =========================update_user_skill============================

@router.put("/{skill_id}",response_model=UserSkillResponse,)

async def update_user_skill(
    skill_id: int,
    user_skill_data: UpdateUserSkill,
    current_user: User = Depends(require_candidate),
    db: AsyncSession = Depends(get_db),
):
    service = UserSkillService(db)

    return await service.update_user_skill(
        current_user.id,
        skill_id,
        user_skill_data,
    )



# =======================delete_user_skill==============================

@router.delete("/{skill_id}",status_code=status.HTTP_204_NO_CONTENT,)

async def delete_user_skill(
    skill_id: int,
    current_user: User = Depends(require_candidate),
    db: AsyncSession = Depends(get_db),
):
    service = UserSkillService(db)

    await service.delete_user_skill(
        current_user.id,
        skill_id,
    )