import uuid

from sqlalchemy import select, text, func, or_, and_
from sqlalchemy.orm import subqueryload

from src.models import tables
from .base import BaseRepository


class ProjectUserRepo(BaseRepository[tables.ProjectUser]):
    table = tables.ProjectUser
