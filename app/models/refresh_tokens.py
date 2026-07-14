from datetime import datetime
from sqlalchemy import Index
from sqlalchemy import (
    String,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from sqlalchemy.sql import func

from app.core.database import Base



class RefreshToken(Base):

    __tablename__ = "refresh_tokens"


    id: Mapped[int] = mapped_column(
        primary_key=True
    )


    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )


    token_hash: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False,
        index=True
    )
    
    jti: Mapped[str] = mapped_column(
    String(36),
    unique=True,
    nullable=False
)


    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )


    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )


    user: Mapped["User"] = relationship(
        "User",
        back_populates="refresh_tokens"
    )
    
    
    __table_args__ = (
    Index(
        "ix_refresh_tokens_user_revoked",
        "user_id",
        "revoked_at",
    ),
)