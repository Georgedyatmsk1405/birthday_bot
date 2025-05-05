```
from fastapi import HTTPException
from app.api.schemas import CustomNotificationSchema
from app.repository.custom_notification import CustomNotificationRepo
from app.repository.group import GroupRepo
from app.bot.utils.auth import tg_auth


class CustomNotificationService:
    @staticmethod
    async def create_notification(data: CustomNotificationSchema, current_user_id: int):
        group = await GroupRepo.find_one_or_none(group_id=data.group_id)
        if not group or group.admin_id != current_user_id:
            raise HTTPException(status_code=403, detail="Permission denied")
        
        return await CustomNotificationRepo.add(**data.dict())

    @staticmethod
    async def update_notification(notification_id: int, data: CustomNotificationSchema, current_user_id: int):
        notification = await CustomNotificationRepo.find_one_or_none(id=notification_id)
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
            
        group = await GroupRepo.find_one_or_none(group_id=notification.group_id)
        if not group or group.admin_id != current_user_id:
            raise HTTPException(status_code=403, detail="Permission denied")
            
        return await CustomNotificationRepo.update(
            filter={"id": notification_id},
            values=data.dict(exclude_unset=True)
        )

    @staticmethod
    async def delete_notification(notification_id: int, current_user_id: int):
        notification = await CustomNotificationRepo.find_one_or_none(id=notification_id)
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
            
        group = await GroupRepo.find_one_or_none(group_id=notification.group_id)
        if not group or group.admin_id != current_user_id:
            raise HTTPException(status_code=403, detail="Permission denied")
            
        return await CustomNotificationRepo.delete(notification_id)

    @staticmethod
    async def get_group_notifications(group_id: int, current_user_id: int):
        group = await GroupRepo.find_one_or_none(group_id=group_id)
        if not group or group.admin_id != current_user_id:
            raise HTTPException(status_code=403, detail="Permission denied")
            
        return await CustomNotificationRepo.find_all(group_id=group_id)
