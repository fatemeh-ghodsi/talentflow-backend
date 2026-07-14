from datetime import date
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class ExperienceBase(BaseModel):

    job_title: str = Field( ..., max_length=150,)

    company_name: str = Field( ...,max_length=150,)

    location: Optional[str] = Field(default=None,max_length=150,)

    start_date: date

    end_date: Optional[date] = None

    is_current: bool = False

    description: Optional[str] = None



class CreateExperience(ExperienceBase):
    pass



class UpdateExperience(BaseModel):

    job_title: Optional[str] = Field( default=None,  max_length=150,)

    company_name: Optional[str] = Field(  default=None,  max_length=150,)

    location: Optional[str] = Field( default=None, max_length=150, )

    start_date: Optional[date] = None

    end_date: Optional[date] = None

    is_current: Optional[bool] = None

    description: Optional[str] = None


class ExperienceResponse(ExperienceBase):

    id: int

    user_id: int

    model_config = ConfigDict( from_attributes=True, )
