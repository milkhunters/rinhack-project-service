from .project import ProjectRepo
from .project_invite import ProjectInviteRepo
from .notification import NotificationRepo
from .project_user import ProjectUserRepo


class RepoFactory:
    def __init__(self, session):
        self._session = session

    @property
    def notification(self) -> NotificationRepo:
        return NotificationRepo(self._session)

    @property
    def project(self) -> ProjectRepo:
        return ProjectRepo(self._session)

    @property
    def project_invite(self) -> ProjectInviteRepo:
        return ProjectInviteRepo(self._session)

    @property
    def project_user(self) -> ProjectUserRepo:
        return ProjectUserRepo(self._session)
