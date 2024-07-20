from pydantic import BaseModel, Field, EmailStr


class TokenData(BaseModel):
    id: str | None = None
