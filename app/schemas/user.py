from datetime import datetime
from pydantic import BaseModel, EmailStr, ConfigDict, Field


class UserCreate(BaseModel):
    """ This class is for creating user"""
    name: str = Field(..., min_length=3, max_length=30, description="User Name", examples=["John Doe"])

    email: EmailStr = Field(..., description="User Email", examples=["user@example.com"])

    avatar_url: str | None = Field(default=None, description="User Avatar URL", examples=["https://example.com/avatar.jpg"])

    provider_id:str = Field(..., description="External auth provider ID for the user", examples=["1234567890"])


class UserResponse(BaseModel):
    """ This class is for returning user"""

    id: int
    name: str
    avatar_url: str | None = None
    email: EmailStr
    updated_at: datetime
    created_at: datetime
    model_config = ConfigDict(
        from_attributes=True
    )


class UserUpdate(BaseModel):
    """ This is for updating user"""
    name: str | None = Field(default=None, min_length=3, max_length=30, description="User Name", examples=["John Doe"])
    avatar_url: str | None = Field(default=None, description="User Avatar URL", examples=["https://example.com/avatar.jpg"])

    