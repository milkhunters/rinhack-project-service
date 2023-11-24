import uuid

from fastapi import APIRouter, Depends
from fastapi import status as http_status

from src.dependencies.services import get_services
from src.models import schemas
from src.services import ServiceFactory
from src.views import ProjectResponse, ProjectsResponse
from views.project import ProjectInviteResponse, ProjectInvitesResponse

router = APIRouter()


@router.get("/list", response_model=ProjectsResponse, status_code=http_status.HTTP_200_OK)
async def project_list(
        page: int = 1,
        per_page: int = 10,
        query: str = None,
        services: ServiceFactory = Depends(get_services)
):
    """
    Получить список проектов, в которых состоит пользователь

    Требуемое состояние: Active

    Требуемые права доступа: GET_PROJECT

    """
    return ProjectsResponse(
        content=await services.project.project_list(page, per_page, query)
    )


@router.post("/new", response_model=ProjectResponse, status_code=http_status.HTTP_201_CREATED)
async def new_project(project: schemas.ProjectCreate, services: ServiceFactory = Depends(get_services)):
    """
    Создать проект

    Требуемое состояние: ACTIVE

    Требуемые права доступа: CREATE_PROJECT

    """
    return ProjectResponse(content=await services.project.create_project(project))


@router.get("/{project_id}", response_model=ProjectResponse, status_code=http_status.HTTP_200_OK)
async def get_project(project_id: uuid.UUID, services: ServiceFactory = Depends(get_services)):
    """
    Получить проект по id

    Требуемое состояние: Active

    Требуемые права доступа: GET_PROJECT
    """
    return ProjectResponse(content=await services.project.get_project(project_id))


@router.put("/{project_id}", response_model=None, status_code=http_status.HTTP_204_NO_CONTENT)
async def update_project(
        project_id: uuid.UUID,
        data: schemas.ProjectUpdate,
        services: ServiceFactory = Depends(get_services)
):
    """
    Обновить проект по id

    Требуемое состояние: ACTIVE

    Требуемые права доступа: UPDATE_PROJECT

    """
    await services.project.update_project(project_id, data)


@router.delete("/{project_id}", response_model=None, status_code=http_status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: uuid.UUID, services: ServiceFactory = Depends(get_services)):
    """
    Удалить проект по id

    Требуемое состояние: ACTIVE

    Требуемые права доступа: DELETE_PROJECT
    """
    await services.project.delete_project(project_id)


@router.post("/{project_id}/invite", response_model=ProjectInviteResponse, status_code=http_status.HTTP_200_OK)
async def invite_to_project(
        project_id: uuid.UUID,
        services: ServiceFactory = Depends(get_services)
):
    """
    Пригласить пользователя в проект

    Требуемое состояние: ACTIVE

    Требуемые права доступа: MAKE_INVITE_LINK

    """
    return ProjectInviteResponse(
        content=await services.project.create_invite_link(project_id)
    )


@router.get("/{project_id}/invite/list", response_model=ProjectInvitesResponse, status_code=http_status.HTTP_200_OK)
async def get_project_invite_links(
        project_id: uuid.UUID,
        services: ServiceFactory = Depends(get_services)
):
    """
    Получить список ссылок-приглашений в проект

    Требуемое состояние: ACTIVE

    Требуемые права доступа: GET_INVITE_LINK

    """
    return ProjectInvitesResponse(
        content=await services.project.project_invite_links(project_id)
    )


@router.delete("/invite/{invite_id}", response_model=None, status_code=http_status.HTTP_204_NO_CONTENT)
async def delete_project_invite_link(
        invite_id: uuid.UUID,
        services: ServiceFactory = Depends(get_services)
):
    """
    Удалить ссылку-приглашение в проект

    Требуемое состояние: ACTIVE

    Требуемые права доступа: DELETE_INVITE_LINK

    """
    await services.project.delete_invite_link(invite_id)


@router.post("/invite/{invite_id}/accept", response_model=None, status_code=http_status.HTTP_204_NO_CONTENT)
async def accept_project_invite_link(
        invite_id: uuid.UUID,
        services: ServiceFactory = Depends(get_services)
):
    """
    Принять приглашение в проект

    Требуемое состояние: ACTIVE

    Требуемые права доступа: ACCEPT_INVITE_LINK

    """
    await services.project.accept_invite_link(invite_id)
