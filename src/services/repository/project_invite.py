import uuid

from sqlalchemy import select, text, func, or_, and_
from sqlalchemy.orm import subqueryload

from src.models import tables
from .base import BaseRepository


class ProjectInviteRepo(BaseRepository[tables.ProjectInvite]):
    table = tables.ProjectInvite

    async def make_link(self, project_id: uuid.UUID) -> uuid.UUID:
        pass
