from datetime import datetime
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

from app.core.enum import (
    WorkMode,
    EmploymentType,
    ExperienceLevel,
)


class JobBase(BaseModel):

    description: Optional[str] = Field(default=None)

    location: Optional[str] = Field(default=None)

    work_mode: WorkMode = Field( default=WorkMode.ONSITE)

    employment_type: EmploymentType = Field(default=EmploymentType.FULL_TIME)

    experience_level: ExperienceLevel = Field(default=ExperienceLevel.JUNIOR )

    is_active: bool = Field(default=True)


class CreateJob(JobBase):

    title: str = Field(..., max_length=150,)

    requirements: str = Field(...)


class UpdateJob(JobBase):
    pass


class JobFilter(BaseModel):

    search: str | None = None

    location: str | None = None

    work_mode: WorkMode | None = None

    employment_type: EmploymentType | None = None

    experience_level: ExperienceLevel | None = None

    is_active: bool | None = None


class JobResponse(JobBase):

    id: int

    company_id: int

    title: str

    requirements: str

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)