from pydantic import BaseModel, Field, EmailStr


class Email(BaseModel):
    email: EmailStr = Field(...)


class Password(BaseModel):
    password: str = Field(..., )
