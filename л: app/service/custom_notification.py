```python
from fastapi import HTTPException
from app.repository.custom_notification import CustomNotificationRepo
from app.api.schemas import CustomNotificationSchema


class CustomNotificationService:
    @staticmethod
    async def create_custom_notification(data: dict):
        schema = CustomNotificationSchema.parse_obj(data)
        await CustomNotificationRepo.add(**schema.dict())

    @staticmethod
    async def update_custom_notification(notification_id: int, data: dict):
        schema = CustomNotificationSchema.parse_obj(data)
        await CustomNotificationRepo.update({"id": notification_id}, schema.dict())

    @staticmethod
    async def delete_custom_notification(notification_id: int):
        await CustomNotificationRepo.delete(notification_id)
```
