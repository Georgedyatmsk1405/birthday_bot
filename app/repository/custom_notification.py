
from app.models.custom_notifications import CustomNotification
from app.repository.base import BaseRepo

class CustomNotificationRepo(BaseRepo):
    model = CustomNotification

    @classmethod
    async def create_custom_notification(cls, *, group_id: int, content: str):
        return await cls.add(group_id=group_id, content=content)

    @classmethod
    async def get_custom_notifications_for_group(cls, group_id: int):
        return await cls.find_all(group_id=group_id)
