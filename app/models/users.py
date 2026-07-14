from typing import List, Optional
from datetime import datetime

from sqlalchemy import String, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.core.enum import UserRole


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    full_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    role: Mapped[UserRole] = mapped_column(
    Enum(
        UserRole,
        values_callable=lambda obj: [e.value for e in obj],
        name="user_role",
    ),
    default=UserRole.CANDIDATE,
    nullable=False,
)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # =====================================================
    # Relationships
    # =====================================================

    profile: Mapped["Profile"] = relationship(
        "Profile",
        back_populates="user",
        cascade="all, delete-orphan",
        uselist=False,
        lazy="selectin",
    )

    applications: Mapped[List["Application"]] = relationship(
        "Application",
        back_populates="user",
        lazy="selectin",
    )

    user_skills: Mapped[List["UserSkill"]] = relationship(
        "UserSkill",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    educations: Mapped[List["Education"]] = relationship(
        "Education",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    experiences: Mapped[List["Experience"]] = relationship(
        "Experience",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    company: Mapped[Optional["Company"]] = relationship(
        "Company",
        back_populates="owner",
        uselist=False,
    )

    refresh_tokens: Mapped[List["RefreshToken"]] = relationship(
        "RefreshToken",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )