from typing import Optional
from datetime import datetime

from sqlalchemy import String, Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Profile(Base):

    __tablename__ = "profiles"


    id: Mapped[int] = mapped_column( primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"),nullable=False,unique=True)


    photo_url: Mapped[Optional[str]] = mapped_column(String(512))


    bio: Mapped[Optional[str]] = mapped_column( Text)


    major: Mapped[Optional[str]] = mapped_column(String(100) )



    resume_url: Mapped[Optional[str]] = mapped_column(String(512) )


    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )


    user: Mapped["User"] = relationship("User",back_populates="profile")
