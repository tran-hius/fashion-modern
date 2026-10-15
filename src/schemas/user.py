from pydantic import BaseModel, EmailStr, ConfigDict, Field
from datetime import datetime

class MessageResponse(BaseModel):
    message: str

class UserCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    username: str = Field(min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9_]+$")
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    model_config = ConfigDict(str_strip_whitespace=True, str_min_length=1)


class UserResponse(BaseModel):
    id: int
    full_name: str
    username: str
    avatar_url: str | None = None
    email: EmailStr
    bio: str | None = None
    role: str  
    address: str | None = None
    phone_number: str | None = None
    is_verify: bool
    is_blocked: bool
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )
    username: str | None = Field(
        default=None,
        min_length=3,
        max_length=30,
        pattern=r"^[a-zA-Z0-9_]+$",
    )
    email: EmailStr | None = None
    bio: str | None = Field(
        default=None,
        max_length=500,
    )
    address: str | None = Field(
        default=None,
        max_length=255,
    )
    phone_number: str | None = Field(
        default=None,
        max_length=20,
    )

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )