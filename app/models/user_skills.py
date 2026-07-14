from datetime import datetime

from sqlalchemy import (
    ForeignKey,
    DateTime,
    Integer,
    CheckConstraint,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.sql import func

from app.core.database import Base


class UserSkill(Base):

    __tablename__ = "user_skills"

    __table_args__ = (
        CheckConstraint(
            "level >= 1 AND level <= 5",
            name="ck_user_skill_level",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    skill_id: Mapped[int] = mapped_column(
        ForeignKey("skills.id"),
        nullable=False,
        index=True,
    )

    level: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    learned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="user_skills",
    )

    skill: Mapped["Skill"] = relationship(
        "Skill",
        back_populates="user_skills",
    )