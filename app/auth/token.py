import hashlib
import secrets
import uuid

from datetime import datetime, timedelta, timezone

from app.core.config import settings


def generate_refresh_token() -> str:
    return secrets.token_urlsafe(64)


def hash_refresh_token( token: str,) -> str:

    return hashlib.sha256(token.encode()).hexdigest()


def create_refresh_token_expire() -> datetime:

    return (datetime.now(timezone.utc) + timedelta( days=settings.REFRESH_TOKEN_EXPIRE_DAYS ))


def generate_jti() -> str:
    return str(uuid.uuid4())