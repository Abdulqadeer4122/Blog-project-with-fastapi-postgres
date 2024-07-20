from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .blog_model import Blog


class User(Base):
    """
    User model.
    """
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    blogs = relationship("Blog", back_populates="author", lazy='joined')
