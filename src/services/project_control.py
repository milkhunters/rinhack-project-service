import uuid

from services.repository import ProjectUserRepo
from src.models.state import NotificationType
from src.protos.project_control import project_control_pb2, project_control_pb2_grpc
from src.services.repository import NotificationRepo


class ProjectService(project_control_pb2_grpc.ProjectServiceServicer):
    def __init__(self, app_state):
        self.db_session = app_state.db_session

    async def SendNotification(self, request, context):
        try:

            owner_id = uuid.UUID(request.owner_id)
            content_id = uuid.UUID(request.content_id)
            content = request.content
            type_id = NotificationType(request.type_id)

            async with self.db_session() as session:
                notification_repo = NotificationRepo(session)
                resp = await notification_repo.create(
                    owner_id=owner_id,
                    type_id=type_id,
                    content_id=content_id,
                    content=content,
                )
                await session.commit()
        except Exception:  # todo: описать конкретные исключения
            return project_control_pb2.NotificationReply(id="Error")
        return project_control_pb2.NotificationReply(id=resp.id)

    async def IsUserInProject(self, request, context):
        try:
            project_id = uuid.UUID(request.project_id)
            user_id = uuid.UUID(request.user_id)
            async with self.db_session() as session:
                project_user_repo = ProjectUserRepo(session)
                resp = await project_user_repo.get(project_id=project_id, user_id=user_id)
            return project_control_pb2.IsUserInProjectReply(result=resp is not None)
        except Exception:  # todo: описать конкретные исключения
            return project_control_pb2.IsUserInProjectReply(result=False)
