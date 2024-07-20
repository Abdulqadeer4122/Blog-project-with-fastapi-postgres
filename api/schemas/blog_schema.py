from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class BaseBlog(BaseModel):
    title: str
    body: str


class BlogContent(BaseBlog):
    pass


class BlogResponse(BaseModel):
    id: UUID
    title: str
    body: str
    created_at: datetime
    author_id: UUID
    author_name: str

    class Config:
        orm_mode = True


class AllBlogResponse(BaseModel):
    id: UUID
    title: str
    body: str
    created_at: datetime

    class Config:
        orm_mode = True
