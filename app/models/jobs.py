from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    String,
    Text,
    DateTime,
    ForeignKey,
    Enum,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.sql import func

from app.core.database import Base
from app.core.enum import (
    WorkMode,
    EmploymentType,
    ExperienceLevel,
)


class Job(Base):

    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        index=True,
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
    )

    requirements: Mapped[Optional[str]] = mapped_column(
        Text,
    )

    location: Mapped[Optional[str]] = mapped_column(
        String(255),
        index=True,
    )

    work_mode: Mapped[WorkMode] = mapped_column(
        Enum(
            WorkMode,
            values_callable=lambda obj: [e.value for e in obj],
            name="work_mode",
        ),
        nullable=False,
        default=WorkMode.ONSITE,
    )

    employment_type: Mapped[EmploymentType] = mapped_column(
        Enum(
            EmploymentType,
            values_callable=lambda obj: [e.value for e in obj],
            name="employment_type",
        ),
        nullable=False,
        default=EmploymentType.FULL_TIME,
    )

    experience_level: Mapped[ExperienceLevel] = mapped_column(
        Enum(
            ExperienceLevel,
            values_callable=lambda obj: [e.value for e in obj],
            name="experience_level",
        ),
        nullable=False,
        default=ExperienceLevel.JUNIOR,
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
        index=True,
    )

    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    company: Mapped["Company"] = relationship(
        "Company",
        back_populates="jobs",
        lazy="selectin",
    )

    applications: Mapped[List["Application"]] = relationship(
        "Application",
        back_populates="job",
        cascade="all, delete-orphan",
        lazy="selectin",
    )