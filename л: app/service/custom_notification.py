```python
from fastapi import HTTPException
from app.repository.custom_notification import CustomNotificationRepo
from app.repository.group import GroupRepo
from app.api.schemas import CustomNotificationCreateSchema, CustomNotificationUpdateSchema


class CustomNotificationService:
    @staticmethod
    async def create_notification(data: CustomNotificationCreateSchema, admin_id: int):
        group = await GroupRepo.find_one_or_none(group_id=data.group_id)
        if not group or group.admin_id != admin_id:
            raise HTTPException(status_code=403, detail="Permission denied")
        
        return await CustomNotificationRepo.add(
            group_id=data.group_id,
            message=data.message
        )

    @staticmethod
    async def update_notification(
        notification_id: int, 
        data: CustomNotificationUpdateSchema, 
        admin_id: int
    ):
        notification = await CustomNotificationRepo.find_one_or_none(id=notification_id)
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
            
        group = await GroupRepo.find_one_or_none(group_id=notification.group_id)
        if not group or group.admin_id != admin_id:
            raise HTTPException(status_code=403, detail="Permission denied")

        return await CustomNotificationRepo.update(
            filter={"id": notification_id},
            values=data.dict(exclude_unset=True)
        )

    @staticmethod
    async def delete_notification(notification_id: int, admin_id: int):
        notification = await CustomNotificationRepo.find_one_or_none(id=notification_id)
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
            
        group = await GroupRepo.find_one_or_none(group_id=notification.group_id)
        if not group or group.admin_id != admin_id:
            raise HTTPException(status_code=403, detail="Permission denied")

        await CustomNotificationRepo.delete(notification_id)
        return {"message": "Notification deleted"}

    @staticmethod
    async def get_group_notifications(group_id: int):
        return await CustomNotificationRepo.get_group_notifications(group_id)
```
