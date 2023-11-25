import uuid

from sqlalchemy import Column, UUID, VARCHAR, DateTime, func
from sqlalchemy.orm import relationship

from src.db import Base


class Project(Base):
    """
    The Project model
    """
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(VARCHAR(64), nullable=False)
    owner_id = Column(UUID(as_uuid=True), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=True)
    end_time = Column(DateTime(timezone=True), nullable=True)
    users = relationship("models.tables.project_user.ProjectUser", back_populates="projects")
    invites = relationship("models.tables.project_invite.ProjectInvite", back_populates="projects")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f'<{self.__class__.__name__}: {self.id}>'
