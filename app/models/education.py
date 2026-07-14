from datetime import date
from typing import Optional

from sqlalchemy import (
    Date,
    Enum,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.core.database import Base
from app.core.enum import EducationLevel


class Education(Base):

    __tablename__ = "educations"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    
    degree: Mapped[EducationLevel] = mapped_column(
    Enum(
        EducationLevel,
        values_callable=lambda obj: [e.value for e in obj],
        name="education_level",
    ),
    nullable=False,
)

    
    institution: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    field_of_study: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    start_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
    )

    end_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
    )

    is_current: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="educations",
    )