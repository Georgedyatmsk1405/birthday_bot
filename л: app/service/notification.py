from fastapi import HTTPException
from app.repository.notification import GroupNotificationRepo
from app.repository.group import GroupRepo
from app.repository.user import UserRepo


class NotificationService:
    @staticmethod
    async def create_notification(content: str, group_id: int, for_user_id: int):
        group = await GroupRepo.find_one_or_none(group_id=group_id)
        if not group:
            raise HTTPException(status_code=404, detail="Group Not Found")
        user = await UserRepo.find_one_or_none(telegram_id=for_user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User Not Found")
        await GroupNotificationRepo.add(
            content=content, group_id=group_id, for_user_id=for_user_id
        )

    @staticmethod
    async def list_notifications(group_id: int):
        return await GroupNotificationRepo.find_all(group_id=group_id)

    @staticmethod
    async def retrieve_notification(notification_id: int):
        return await GroupNotificationRepo.find_one_or_none(id=notification_id)

    @staticmethod
    async def update_notification(notification_id: int, content: str):
        notification = await GroupNotificationRepo.find_one_or_none(id=notification_id)
        if not notification:
            raise HTTPException(status_code=404, detail="Notification Not Found")
        await GroupNotificationRepo.update({"id": notification_id}, {"content": content})

    @staticmethod
    async def delete_notification(notification_id: int):
        await GroupNotificationRepo.delete(p_id=notification_id)

===
Конец файла ===