```
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.repository.base import BaseRepo
from app.models import CustomNotification
from app.database import async_session_maker


class CustomNotificationRepo(BaseRepo):
    model = CustomNotification

    @classmethod
    async def find_all_active(cls, group_id: int):
        async with async_session_maker() as session:
            query = (
                select(cls.model)
                .filter_by(group_id=group_id, is_active=True)
                .options(selectinload(cls.model.group))
            result = await session.execute(query)
            return result.scalars().all()

```
