import uuid

from sqlalchemy import select, or_, and_

from src.models import tables
from .base import BaseRepository


class ProjectRepo(BaseRepository[tables.Project]):
    table = tables.Project

    async def search(
            self,
            query: str,
            fields: list[str],
            limit: int = 100,
            offset: int = 0,
            include_user_id: uuid.UUID = None,
            **kwargs
    ) -> list[tables.Project]:
        return await self.__get_range(
            query=query,
            fields=fields,
            limit=limit,
            offset=offset,
            include_user_id=include_user_id,
            **kwargs
        )

    async def get_all(
            self, limit: int = 100,
            offset: int = 0,
            include_user_id: uuid.UUID = None,
            **kwargs
    ) -> list[tables.Project]:
        return await self.__get_range(
            limit=limit,
            offset=offset,
            include_user_id=include_user_id,
            **kwargs
        )

    async def get(self, **kwargs) -> tables.Project:
        stmt = select(self.table).filter_by(**kwargs)
        return (await self._session.execute(stmt)).scalars().first()

    async def __get_range(
            self,
            *,
            query: str = None,
            fields: list[str] = None,
            limit: int = 100,
            offset: int = 0,
            include_user_id: uuid.UUID = None,
            **kwargs
    ) -> list[tables.Project]:

        # Основной запрос
        stmt = (
            select(
                self.table
            )
        )

        # Выборка
        if include_user_id:
            stmt = stmt.join(
                tables.ProjectUser,
                self.table.id == tables.ProjectUser.project_id
            ).where(
                tables.ProjectUser.user_id == include_user_id
            )

        # Лимиты и смещения
        stmt = stmt.limit(limit).offset(offset)

        # Фильтры kwargs
        stmt = stmt.where(
            and_(*[getattr(self.table, field) == value for field, value in kwargs.items()])
        )

        # Поиск
        if query and fields:
            stmt = stmt.where(
                or_(*[getattr(self.table, field).ilike(f"%{query}%") for field in fields])
            )

        result = await self._session.execute(stmt)
        return result.scalars().all()
