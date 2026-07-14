from datetime import date
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

from app.core.enum import EducationLevel


class EducationBase(BaseModel):

    institution: str = Field(  ..., max_length=150,)

    field_of_study: str = Field( ...,max_length=150, )

    degree: EducationLevel

    start_date: date

    end_date: Optional[date] = None

    is_current: bool = False

    description: Optional[str] = None


class CreateEducation(EducationBase):
    pass


class UpdateEducation(BaseModel):

    institution: Optional[str] = None

    field_of_study: Optional[str] = None

    degree: Optional[EducationLevel] = None

    start_date: Optional[date] = None

    end_date: Optional[date] = None

    is_current: Optional[bool] = None

    description: Optional[str] = None


class EducationResponse(EducationBase):

    id: int

    user_id: int

    model_config = ConfigDict(from_attributes=True,)