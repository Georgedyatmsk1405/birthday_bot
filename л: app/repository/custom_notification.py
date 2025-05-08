```python
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.repository.base import BaseRepo
from app.models import CustomNotification


class CustomNotificationRepo(BaseRepo):
    model = CustomNotification

    @classmethod
    async def get_group_notifications(cls, group_id: int):
        return await cls.find_all(group_id=group_id)

    @classmethod
    async def get_active_group_notifications(cls, group_id: int):
        return await cls.find_all(group_id=group_id, is_active=True)
```
