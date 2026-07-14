from sqlalchemy.ext.asyncio import AsyncSession

from app.common.pagination import Pagination
from app.common.responses import PaginatedResponse, PaginationMetadata
from app.repositories import user_repository
from app.schemas.user import UserOut


class AdminService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ======================Get All Users=====================

    async def get_all_users(
        self, pagination: Pagination
    ) -> PaginatedResponse[UserOut]:
        users, total = await user_repository.get_all_users(
            offset=pagination.offset,
            limit=pagination.limit,
            db=self.db,
        )

        metadata = PaginationMetadata(
            total_items=total,
            total_pages=(total + pagination.size - 1) // pagination.size,
            current_page=pagination.page,
            page_size=pagination.size,
        )

        return PaginatedResponse(
            items=[UserOut.model_validate(user) for user in users],
            metadata=metadata,
        )
