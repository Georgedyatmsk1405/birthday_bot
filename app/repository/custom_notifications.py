
from app.models.custom_notifications import CustomNotification
from app.repository.base import BaseRepo


class CustomNotificationsRepo(BaseRepo):
    model = CustomNotification

    @classmethod
    async def create_custom_notification(cls, **values):
        return await cls.add(**values)

    @classmethod
    async def get_custom_notification(cls, notification_id: int):
        return await cls.find_one_or_none_by_id(notification_id)

    @classmethod
    async def list_custom_notifications(cls, group_id: int):
        return await cls.find_all(group_id=group_id)

    @classmethod
    async def update_custom_notification(cls, notification_id: int, **values):
        return await cls.update({"id": notification_id}, values)

    @classmethod
    async def delete_custom_notification(cls, notification_id: int):
        return await cls.delete(notification_id)
