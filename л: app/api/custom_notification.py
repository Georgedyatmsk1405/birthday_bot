```python
from fastapi import APIRouter, Depends, HTTPException
from app.bot.utils.auth import tg_auth
from app.api.schemas import (
    CustomNotificationCreate,
    CustomNotificationUpdate,
    CustomNotificationResponse
)
from app.service.custom_notification import CustomNotificationService

router = APIRouter(prefix="/custom_notifications", tags=["Custom Notifications"])


@router.post("/", response_model=CustomNotificationResponse)
async def create_notification(
    data: CustomNotificationCreate,
    admin_id: int = Depends(tg_auth)
):
    return await CustomNotificationService.create_notification(data, admin_id)


@router.put("/{notification_id}", response_model=CustomNotificationResponse)
async def update_notification(
    notification_id: int,
    data: CustomNotificationUpdate,
    admin_id: int = Depends(tg_auth)
):
    return await CustomNotificationService.update_notification(
        notification_id, data, admin_id
    )


@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: int,
    admin_id: int = Depends(tg_auth)
):
    return await CustomNotificationService.delete_notification(notification_id, admin_id)


@router.get("/group/{group_id}", response_model=list[CustomNotificationResponse])
async def get_group_notifications(
    group_id: int,
    admin_id: int = Depends(tg_auth)
):
    group = await GroupRepo.find_one_or_none(group_id=group_id)
    if not group or group.admin_id != admin_id:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    return await CustomNotificationService.get_group_notifications(group_id)


@router.get("/group/{group_id}/active", response_model=list[CustomNotificationResponse])
async def get_active_group_notifications(group_id: int):
    return await CustomNotificationService.get_active_group_notifications(group_id)
```
