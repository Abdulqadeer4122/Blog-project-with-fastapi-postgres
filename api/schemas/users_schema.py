from typing import List
from pydantic import BaseModel, Field, EmailStr
from uuid import UUID


class BaseUser(BaseModel):
    username: str = Field(...)
    email: EmailStr = Field(...)


class User(BaseUser):
    password: str = Field(...)


class UserResponse(BaseUser):
    id: UUID

    class Config:
        from_attributes = True
