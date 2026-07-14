from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProfileBase(BaseModel):
    bio: Optional[str] = Field(default=None)
    major: Optional[str] = Field(default=None)


class CreateProfile(ProfileBase):
    pass


class UpdateProfile(ProfileBase):
    pass


class ProfileResponse(ProfileBase):
    id: int
    user_id: int

    photo_url: Optional[str] = None
    resume_url: Optional[str] = None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)