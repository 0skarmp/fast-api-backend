from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserRegisterDto(BaseModel):
    name: str = Field(min_length=3, max_length=15)
    lastname: str = Field(min_length=3, max_length=15)
    email: EmailStr
    number: str = Field(
        min_length=3,
        max_length=15,
        pattern=r"^\+?[0-9]+$",
    )
    password: str = Field(min_length=8, max_length=128)


class UserResponseDto(BaseModel):
    id: str
    name: str
    lastname: str
    email: EmailStr
    number: str
    is_active: bool
    created_at: datetime


class UserRegisterResponseDto(BaseModel):
    message: str
    user: UserResponseDto
