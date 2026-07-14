from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.core.enum import UserRole


# Base
# =====================================================

class UserBase(BaseModel):

    email: EmailStr

    full_name: str = Field(...,min_length=3, max_length=100, )


# Create
# =====================================================

class UserCreate(UserBase):

    password: str = Field(..., min_length=8,max_length=100,)


# Login
# =====================================================

class UserLogin(BaseModel):

    email: EmailStr

    password: str = Field(..., min_length=8, max_length=100,)


# Update
# =====================================================

class UserUpdate(BaseModel):

    full_name: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=100,
    )


# Response
# =====================================================

class UserOut(UserBase):

    id: int

    role: UserRole

    created_at: datetime

    model_config = ConfigDict(from_attributes=True,)


# Change Password
# =====================================================

class PasswordChangeRequest(BaseModel):

    old_password: str = Field(...,min_length=8,max_length=100, )

    new_password: str = Field(..., min_length=8, max_length=100,)