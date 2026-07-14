from sqlalchemy.ext.asyncio import AsyncSession

from app.common.pagination import Pagination
from app.common.responses import (
    PaginatedResponse,
    PaginationMetadata,
)

from app.exceptions import NotFoundError

from app.models.skills import Skill

from app.repositories import skill_repository

from app.schemas.skill import SkillResponse


class SkillService:

    def __init__(  self,db: AsyncSession,):
        self.db = db


    # ====================get_by_id==============================

    async def get_by_id(
        self,
        skill_id: int,
    ) -> Skill:

        skill = await skill_repository.get_by_id(skill_id,self.db,)

        if skill is None:
            raise NotFoundError("Skill not found.")

        return skill

   
    # ====================search_skills============================

    async def search_skills(
        self,
        search: str,
        pagination: Pagination,
    ) -> PaginatedResponse[SkillResponse]:

        search = search.strip()

        skills, total = await skill_repository.search_skills(
            search=search,
            offset=pagination.offset,
            limit=pagination.limit,
            db=self.db,
        )

        page_size = max(pagination.size, 1)

        metadata = PaginationMetadata(
            total_items=total,
            total_pages=(total + page_size - 1) // page_size,
            current_page=pagination.page,
            page_size=page_size,
        )

        return PaginatedResponse(
            items=skills,
            metadata=metadata,
        )