from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CompanyBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    location: Optional[str] = None
    website_url: Optional[str] = None
    logo_url: Optional[str] = None


class CreateCompany(CompanyBase):
    pass


class UpdateCompany(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    website_url: Optional[str] = None
    logo_url: Optional[str] = None


class CompanyResponse(CompanyBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)