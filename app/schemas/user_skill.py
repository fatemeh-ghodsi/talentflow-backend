from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class CreateUserSkill(BaseModel):

    skill_id: int = Field(...)

    level: int = Field(
        default=1,
        ge=1,
        le=5,
    )


class UpdateUserSkill(BaseModel):

    level: int | None = Field(
        default=None,
        ge=1,
        le=5,
    )


class UserSkillResponse(BaseModel):

    id: int

    user_id: int

    skill_id: int

    level: int

    learned_at: datetime

    model_config = ConfigDict(from_attributes=True,)