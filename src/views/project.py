from .base import BaseView
from src.models import schemas


class ProjectResponse(BaseView):
    content: schemas.Project


class ProjectsResponse(BaseView):
    content: list[schemas.Project]


class ProjectInviteResponse(BaseView):
    content: schemas.ProjectInvite


class ProjectInvitesResponse(BaseView):
    content: list[schemas.ProjectInvite]
