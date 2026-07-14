from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.core.enum import ApplicationStatus



class UpdateApplicationStatus(BaseModel):
    status: ApplicationStatus = Field(...)


class ApplicationResponse(BaseModel):

    id: int
    user_id: int
    job_id: int

    status: ApplicationStatus

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict( from_attributes=True)