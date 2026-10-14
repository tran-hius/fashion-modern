from pydantic import BaseModel, EmailStr, ConfigDict, Field


class UserCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr

    password: str = Field(min_length=8, max_length=128)
    model_config = ConfigDict(str_strip_whitespace=True, str_min_length=1)


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str  
    address: str | None = None
    phone_number: str | None = None
    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )
    email: EmailStr | None = None
    address: str | None = Field(
        default=None,
        max_length=255,
    )
    phone_number: str | None = Field(
        default=None,
        max_length=20,
    )
    model_config = ConfigDict(extra="forbid")