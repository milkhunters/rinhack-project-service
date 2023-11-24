from src.models.auth import BaseUser
from . import auth
from . import repository
from .project import ProjectApplicationService
from .notification import NotificationApplicationService
from .permission import PermissionApplicationService
from .stats import StatsApplicationService


class ServiceFactory:
    def __init__(
            self,
            repo_factory: repository.RepoFactory,
            *,
            current_user: BaseUser,
            config,
    ):
        self._repo = repo_factory
        self._current_user = current_user
        self._config = config

    @property
    def project(self) -> ProjectApplicationService:
        return ProjectApplicationService(
            self._current_user,
            project_repo=self._repo.project,
            project_invite_repo=self._repo.project_invite,
            project_user_repo=self._repo.project_user,
        )

    @property
    def notification(self) -> NotificationApplicationService:
        return NotificationApplicationService(self._current_user, notify_repo=self._repo.notification)

    @property
    def stats(self) -> StatsApplicationService:
        return StatsApplicationService(config=self._config)

    @property
    def permission(self) -> PermissionApplicationService:
        return PermissionApplicationService()
