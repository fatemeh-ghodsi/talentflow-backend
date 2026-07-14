from datetime import datetime, timezone

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.security import (
    verify_password,
    get_password_hash,
    create_access_token,
)

from app.auth.token import (
    generate_refresh_token,
    hash_refresh_token,
    create_refresh_token_expire,
    generate_jti,
)

from app.core.logger import logger

from app.exceptions import (
    InvalidCredentials,
    NotFoundError,
)

from app.models.refresh_tokens import RefreshToken

from app.repositories import (
    user_repository,
    refresh_token_repository,
)

from app.schemas.user import (
    UserCreate,
    PasswordChangeRequest,
)

from app.schemas.auth import (
    Token,
    RefreshTokenRequest,
)

from app.services.user import UserService


class AuthService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.user_service = UserService(db)

   
    # ========================= Register============================

    async def register(self,user_data: UserCreate, ):

        user = await self.user_service.create_user( user_data  )

        logger.info( f"User registered. user_id={user.id}")

        return user

    
    
    # ====================Login=================================

    async def login(self,form_data: OAuth2PasswordRequestForm,) -> Token:

        email = form_data.username.lower().strip()

        user = await user_repository.get_by_email(
            email,
            self.db,
        )

        if user is None:

            logger.warning( f"Login failed. email={email}")

            raise InvalidCredentials( "Invalid email or password"  )
        print("USERNAME:", form_data.username)
        print("PASSWORD:", form_data.password)
        print("HASH:", user.password_hash)
        print(
    "VERIFY:",
    verify_password(
        form_data.password,
        user.password_hash,
    ),
)

        if not verify_password(
            form_data.password,
            user.password_hash,):

            logger.warning(  f"Login failed. email={email}"  )

            raise InvalidCredentials( "Invalid email or password" )

        jti = generate_jti()

        access_token = create_access_token( subject=user.id, jti=jti,)

        raw_refresh_token = generate_refresh_token()

        hashed_refresh_token = hash_refresh_token(raw_refresh_token)

        refresh_model = RefreshToken(
            user_id=user.id,
            jti=jti,
            token_hash=hashed_refresh_token,
            expires_at=create_refresh_token_expire(),
        )

        await refresh_token_repository.create(refresh_model,self.db,)

        logger.info( f"User login. user_id={user.id}")

        return Token(
            access_token=access_token,
            refresh_token=raw_refresh_token,
            token_type="bearer",
        )

    # ========================Refresh Token==========================

    async def refresh(self, refresh_request: RefreshTokenRequest,) -> Token:

        hashed_token = hash_refresh_token( refresh_request.refresh_token )

        token = await refresh_token_repository.get_active_by_hash(
            hashed_token,
            self.db,
        )

        if token is None:
            raise InvalidCredentials( "Invalid refresh token" )

        if token.expires_at < datetime.now(timezone.utc):
            raise InvalidCredentials("Refresh token expired")

        user = await user_repository.get_by_id( token.user_id,self.db,)

        if user is None:
            raise NotFoundError("User not found")

        # Token Rotation
        await refresh_token_repository.revoke(token, self.db,)

        new_jti = generate_jti()

        access_token = create_access_token(
            subject=user.id,
            jti=new_jti,
        )

        raw_refresh_token = generate_refresh_token()

        hashed_refresh_token = hash_refresh_token( raw_refresh_token)

        await refresh_token_repository.create(
            RefreshToken(
                user_id=user.id,
                jti=new_jti,
                token_hash=hashed_refresh_token,
                expires_at=create_refresh_token_expire(),
            ),
            self.db,
        )

        logger.info( f"Refresh token rotated. user_id={user.id}"  )

        return Token(
            access_token=access_token,
            refresh_token=raw_refresh_token,
            token_type="bearer",
        )

     
    # ======================Logout===============================

    async def logout(
        self,
        refresh_token: str,
    ) -> None:

        hashed_token = hash_refresh_token(
            refresh_token
        )

        token = await refresh_token_repository.get_active_by_hash(
            hashed_token,
            self.db,
        )

        if token is None:
            raise InvalidCredentials("Invalid refresh token" )

        await refresh_token_repository.revoke( token,self.db,  )

        logger.info( f"User logout. user_id={token.user_id}" )

    
    # =================Change Password==================================

    async def change_password(
        self,
        user_id: int,
        password_data: PasswordChangeRequest,
    ) -> None:

        user = await user_repository.get_by_id(
            user_id,
            self.db,
        )

        if user is None:
            raise NotFoundError("User not found" )

        if not verify_password(
            password_data.old_password,
            user.password_hash,
        ):
            raise InvalidCredentials( "Old password is incorrect" )

        await user_repository.update_user(
            user,
            self.db,
            {"password_hash": get_password_hash(password_data.new_password )},
        )

        await refresh_token_repository.revoke_all_user_tokens(user.id,self.db,  )

        logger.info( f"Password changed. user_id={user.id}")