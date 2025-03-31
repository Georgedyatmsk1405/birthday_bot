
from app.repository.custom_notifications import CustomNotificationsRepo


class CustomNotificationsService:
    @staticmethod
    async def create(title: str, content: str, group_id: int):
        return await CustomNotificationsRepo.create_custom_notification(
            title=title, content=content, group_id=group_id
        )

    @staticmethod
    async def retrieve(notification_id: int):
        return await CustomNotificationsRepo.get_custom_notification(notification_id)

    @staticmethod
    async def list(group_id: int):
        return await CustomNotificationsRepo.list_custom_notifications(group_id)

    @staticmethod
    async def update(notification_id: int, title: str, content: str):
        return await CustomNotificationsRepo.update_custom_notification(
            notification_id, title=title, content=content
        )

    @staticmethod
    async def delete(notification_id: int):
        return await CustomNotificationsRepo.delete_custom_notification(notification_id)
