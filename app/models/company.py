from typing import List, Optional
from datetime import datetime
from sqlalchemy import String, Text,DateTime,func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

from typing import List, Optional

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Company(Base):

    __tablename__ = "companies"


    id: Mapped[int] = mapped_column(
        primary_key=True
    )


    owner_id = mapped_column(
    ForeignKey("users.id"),
    unique=True,
    nullable=False,
    index=True,
)


    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        index=True
    )


    description: Mapped[Optional[str]] = mapped_column(
        Text
    )


    location: Mapped[Optional[str]] = mapped_column(
        String(255),
        index=True
    )


    website_url: Mapped[Optional[str]] = mapped_column(
        String(255)
    )


    logo_url: Mapped[Optional[str]] = mapped_column(
        String(255)
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )


    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )


    owner: Mapped["User"] = relationship(
        "User",
        back_populates="company"
    )


    jobs: Mapped[List["Job"]] = relationship(
        "Job",
        back_populates="company",
        cascade="all, delete-orphan",
        lazy="selectin"
    )