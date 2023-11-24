import uuid
from datetime import datetime

from pydantic import BaseModel, field_validator


class Project(BaseModel):
    id: uuid.UUID
    title: str
    owner_id: uuid.UUID

    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True


class ProjectCreate(BaseModel):
    title: str

    @field_validator('title')
    def title_must_be_valid(cls, value):
        if not value:
            raise ValueError("Заголовок не может быть пустым")

        if len(value) > 64:
            raise ValueError("Заголовок не может содержать больше 255 символов")
        return value


class ProjectUpdate(BaseModel):
    title: str = None

    class Config:
        extra = 'ignore'

    @field_validator('title')
    def title_must_be_valid(cls, value):
        if value and len(value) > 64:
            raise ValueError("Название не может содержать больше 64 символов")
        return value


class ProjectInvite(BaseModel):
    id: uuid.UUID

    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True
