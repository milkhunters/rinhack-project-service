import uuid

from sqlalchemy import Column, UUID, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from src.db import Base


class ProjectUser(Base):
    """
    The ProjectUser model
    """
    __tablename__ = "project_users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    projects = relationship("models.tables.project.Project", back_populates="users")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.id}>'
