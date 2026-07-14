from typing import Optional
from datetime import date

from sqlalchemy import (
    String,
    Text,
    ForeignKey,
    Date,
    Boolean,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.core.database import Base


class Experience(Base):

    __tablename__ = "experiences"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    job_title: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    company_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    location: Mapped[Optional[str]] = mapped_column(
        String(150),
        nullable=True,
    )

    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    end_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
    )

    is_current: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="experiences",
    )