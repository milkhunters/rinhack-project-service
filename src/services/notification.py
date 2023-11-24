import uuid

from src.models import schemas
from src.models.permission import Permission
from src.models.auth import BaseUser
from src import exceptions
from src.models.state import UserState
from src.services.auth.filters import state_filter
from src.services.auth.filters import permission_filter
from src.services.repository import NotificationRepo


class NotificationApplicationService:

    def __init__(
            self,
            current_user: BaseUser,
            notify_repo: NotificationRepo
    ):
        self._current_user = current_user
        self._repo = notify_repo

    @permission_filter(Permission.GET_NOTIFICATION)
    @state_filter(UserState.ACTIVE)
    async def get_notifications(self, page: int, per_page: int = 10) -> list[schemas.Notification]:
        """
        Список уведомлений

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

        # Подготовка выходных данных
        notifications = await self._repo.get_all(
            limit=per_page,
            offset=offset,
            order_by="created_at",
            owner_id=self._current_user.id
        )
        return [schemas.Notification.model_validate(notification) for notification in notifications]

    @permission_filter(Permission.GET_NOTIFICATION)
    @state_filter(UserState.ACTIVE)
    async def get_total(self) -> int:
        """
        Количество уведомлений пользователя

        :return:
        """
        return await self._repo.count(owner_id=self._current_user.id)

    @permission_filter(Permission.DELETE_NOTIFICATION)
    @state_filter(UserState.ACTIVE)
    async def delete_notification(self, notification_id: uuid.UUID) -> None:
        """
        Удалить уведомление

        :param notification_id:
        :return:

        """
        notification = await self._repo.get(id=notification_id)
        if not notification:
            raise exceptions.NotFound("Уведомление не найдено")

        if notification.owner_id != self._current_user.id:
            raise exceptions.AccessDenied("Вы не являетесь владельцем уведомления")

        await self._repo.delete(id=notification_id)
