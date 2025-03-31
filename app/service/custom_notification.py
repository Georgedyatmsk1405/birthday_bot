
from app.repository.custom_notification import CustomNotificationRepo

class CustomNotificationService:
    @staticmethod
    async def create_custom_notification(*, group_id: int, content: str):
        return await CustomNotificationRepo.create_custom_notification(group_id=group_id, content=content)

    @staticmethod
    async def get_custom_notifications_for_group(group_id: int):
        return await CustomNotificationRepo.get_custom_notifications_for_group(group_id=group_id)
