from app.models import GroupNotification
from app.repository.base import BaseRepo
from sqlalchemy.future import select
from app.database import async_session_maker
from sqlalchemy.orm import selectinload


class GroupNotificationRepo(BaseRepo):
    model = GroupNotification

    @classmethod
    async def find_all(cls, **filter_by):

        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .filter_by(**filter_by)
                .options(
                    selectinload(cls.model.group), selectinload(cls.model.for_user)
                )
            )
            result = await session.execute(query)
            return result.scalars().all()
