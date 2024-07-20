from sqlalchemy import Boolean, Column, Integer, String, DateTime,ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from sqlalchemy.sql import func


class Blog(Base):
    """
    Blog model.
    """
    __tablename__ = "blogs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    body = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, server_default=func.now())
    author_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)

    author = relationship("User", back_populates="blogs",lazy='joined')
