from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import User
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.common.pagination import Pagination
from app.common.responses import PaginatedResponse, PaginationMetadata
from app.repositories import user_repository
from app.auth.security import get_password_hash
from app.exceptions import ConflictError, NotFoundError
from app.core.logger import logger


class UserService:

    def __init__(self, db: AsyncSession):
        self.db = db

    # ======================= Create User =====================

    async def create_user(self, user_data: UserCreate) -> User:
        email = user_data.email.lower().strip()

        existing_user = await user_repository.get_by_email(email, self.db)
        if existing_user:
            logger.warning(f"User creation failed. Email exists: {email}")
            raise ConflictError("Email already exists")

        user = User(
            email=email,
            full_name=user_data.full_name,
            password_hash=get_password_hash(user_data.password),
        )

        created = await user_repository.create(user, self.db)
        logger.info(f"User created. id={created.id}")
        return created

    # ===================== Get One =========================

    async def get_user(self, user_id: int) -> User:
        user = await user_repository.get_by_id(user_id, self.db)
        if user is None:
            raise NotFoundError(f"User with ID {user_id} not found")
        return user

    # ===================== Get All Users ===================

    async def get_all_users(self, pagination: Pagination) -> PaginatedResponse[UserOut]:
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

        return PaginatedResponse[UserOut](
            items=[UserOut.model_validate(user) for user in users],
            metadata=metadata,
        )

    # ========================== Update User ===========================

    async def update_user(self, user_id: int, user_data: UserUpdate) -> User:
        user = await self.get_user(user_id)

        update_data = user_data.model_dump(
            exclude_unset=True,
            exclude_none=True,
        )

        if not update_data:
            return user

        updated = await user_repository.update_user(user, self.db, update_data)
        logger.info(f"User updated. id={user_id}")
        return updated

    # ====================== Delete User ===============================

    async def delete_user(self, user_id: int) -> bool:
        user = await self.get_user(user_id)
        result = await user_repository.delete_user(user, self.db)
        logger.info(f"User deleted. id={user_id}")
        return result
