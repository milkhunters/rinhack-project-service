import uuid

from src.services.repository import ProjectUserRepo
from src import exceptions
from src.models import schemas
from src.models.permission import Permission
from src.models.auth import BaseUser
from src.models.state import UserState
from src.services.auth.filters import state_filter
from src.services.auth.filters import permission_filter
from src.services.repository import ProjectRepo
from src.services.repository import ProjectInviteRepo


class ProjectApplicationService:

    def __init__(
            self,
            current_user: BaseUser,
            project_repo: ProjectRepo,
            project_invite_repo: ProjectInviteRepo,
            project_user_repo: ProjectUserRepo
    ):
        self._current_user = current_user
        self._repo = project_repo
        self._invite_repo = project_invite_repo
        self._project_user_repo = project_user_repo

    @state_filter(UserState.ACTIVE)
    @permission_filter(Permission.GET_PROJECT)
    async def project_list(
            self,
            page: int = 1,
            per_page: int = 10,
            query: str = None,
    ) -> list[schemas.Project]:
        """
        Получить список проектов

        :param page: номер страницы (всегда >= 1)
        :param per_page: количество проектов на странице (всегда >= 1, но <= per_page_limit)
        :param query: поисковый запрос (если необходим)
        :return:

        """

        if page < 1:
            raise exceptions.NotFound("Страница не найдена")
        if per_page < 1:
            raise exceptions.BadRequest("Неверное количество элементов на странице")

        per_page_limit = 40

        # Подготовка входных данных
        per_page = min(per_page, per_page_limit, 2147483646)
        offset = min((page - 1) * per_page, 2147483646)

        # Выполнение запроса
        if query:
            projects = await self._repo.search(
                query=query,
                fields=["title"],
                limit=per_page,
                offset=offset
            )
        else:
            projects = await self._repo.get_all(
                limit=per_page,
                offset=offset
            )
        return [schemas.Project.model_validate(project) for project in projects]

    @state_filter(UserState.ACTIVE)
    @permission_filter(Permission.GET_PROJECT)
    async def get_project(self, project_id: uuid.UUID) -> schemas.Project:
        project = await self._repo.get(id=project_id)
        if not project:
            raise exceptions.NotFound("Проект не найден")

        _ = await self._project_user_repo.get(
            project_id=project.id,
            user_id=self._current_user.id
        )
        if not _:
            raise exceptions.AccessDenied("Вы не состоите в проекте")

        return schemas.Project.model_validate(project)

    @state_filter(UserState.ACTIVE)
    @permission_filter(Permission.CREATE_PROJECT)
    async def create_project(self, data: schemas.ProjectCreate) -> schemas.Project:
        project = await self._repo.create(
            **data.model_dump(),
            owner_id=self._current_user.id
        )

        await self._project_user_repo.create(
            project_id=project.id,
            user_id=self._current_user.id
        )

        return schemas.Project.model_validate(project)

    @state_filter(UserState.ACTIVE)
    @permission_filter(Permission.UPDATE_PROJECT)
    async def update_project(self, project_id: uuid.UUID, data: schemas.ProjectUpdate) -> None:
        project = await self._repo.get(id=project_id)
        if not project:
            raise exceptions.NotFound("Проект не найден")

        if project.owner_id != self._current_user.id:
            raise exceptions.BadRequest("Вы не являетесь владельцем проекта")

        await self._repo.update(project_id, **data.model_dump())

    @state_filter(UserState.ACTIVE)
    @permission_filter(Permission.DELETE_PROJECT)
    async def delete_project(self, project_id: uuid.UUID) -> None:
        project = await self._repo.get(id=project_id)
        if not project:
            raise exceptions.NotFound("Проект не найден")

        if project.owner_id != self._current_user.id:
            raise exceptions.AccessDenied("Вы не являетесь владельцем проекта")

        await self._repo.delete(id=project_id)

    @state_filter(UserState.ACTIVE)
    @permission_filter(Permission.MAKE_INVITE_LINK)
    async def create_invite_link(self, project_id: uuid.UUID) -> schemas.ProjectInvite:
        project = await self._repo.get(id=project_id)
        if not project:
            raise exceptions.NotFound("Проект не найден")

        if project.owner_id != self._current_user.id:
            raise exceptions.AccessDenied("Вы не являетесь владельцем проекта")

        invite = await self._invite_repo.create(
            project_id=project_id,
            owner_id=self._current_user.id
        )
        return schemas.ProjectInvite.model_validate(invite)

    @state_filter(UserState.ACTIVE)
    @permission_filter(Permission.GET_INVITE_LINK)
    async def project_invite_links(self, project_id: uuid.UUID) -> list[schemas.ProjectInvite]:
        project = await self._repo.get(id=project_id)
        if not project:
            raise exceptions.NotFound("Проект не найден")

        if project.owner_id != self._current_user.id:
            raise exceptions.AccessDenied("Вы не являетесь владельцем проекта")

        invites = await self._invite_repo.get_all(
            project_id=project_id
        )
        return [schemas.ProjectInvite.model_validate(invite) for invite in invites]

    @state_filter(UserState.ACTIVE)
    @permission_filter(Permission.DELETE_INVITE_LINK)
    async def delete_invite_link(self, invite_id: uuid.UUID) -> None:
        invite = await self._invite_repo.get(id=invite_id)
        if not invite:
            raise exceptions.NotFound("Приглашение не найдено")

        project = await self._repo.get(id=invite.project_id)
        if not project:
            raise exceptions.NotFound("Проект не найден")

        if project.owner_id != self._current_user.id:
            raise exceptions.AccessDenied("Вы не являетесь владельцем приглашения")

        await self._invite_repo.delete(id=invite_id)

    @state_filter(UserState.ACTIVE)
    @permission_filter(Permission.ACCEPT_INVITE_LINK)
    async def accept_invite_link(self, invite_id: uuid.UUID) -> None:
        invite = await self._invite_repo.get(id=invite_id)
        if not invite:
            raise exceptions.NotFound("Приглашение не найдено")

        project = await self._repo.get(id=invite.project_id)
        if not project:
            raise exceptions.NotFound("Проект не найден")

        _ = await self._project_user_repo.get(
            project_id=project.id,
            user_id=self._current_user.id
        )
        if _:
            raise exceptions.BadRequest(f"Вы уже состоите в проекте {project.title}")

        await self._project_user_repo.create(
            project_id=project.id,
            user_id=self._current_user.id
        )
