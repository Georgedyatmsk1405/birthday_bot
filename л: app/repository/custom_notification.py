```python
from sqlalchemy import select
from app.models import CustomNotification
from app.repository.base import BaseRepo
from app.database import async_session_maker


class CustomNotificationRepo(BaseRepo):
    model = CustomNotification

    @classmethod
    async def get_group_notifications(cls, group_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(group_id=group_id, is_active=True)
            result = await session.execute(query)
            return result.scalars().all()
```
