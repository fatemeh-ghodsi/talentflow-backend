from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    DateTime,
    Enum,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.sql import func

from app.core.database import Base
from app.core.enum import ApplicationStatus


class Application(Base):
    __tablename__ = "applications"

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "job_id",
            name="uq_application_user_job",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    job_id: Mapped[int] = mapped_column(
        ForeignKey("jobs.id"),
        nullable=False,
        index=True,
    )
    
    status: Mapped[ApplicationStatus] = mapped_column(
    Enum(
        ApplicationStatus,
        values_callable=lambda obj: [e.value for e in obj],
        name="application_status",
    ),
    default=ApplicationStatus.PENDING,
    nullable=False,
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

    user: Mapped["User"] = relationship(
        "User",
        back_populates="applications",
    )

    job: Mapped["Job"] = relationship(
        "Job",
        back_populates="applications",
    )