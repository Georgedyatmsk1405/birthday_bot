```
from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from app.api.schemas import CustomNotificationSchema
from app.bot.utils.auth import tg_auth
from app.service.custom_notification import CustomNotificationService

router = APIRouter(prefix="/api/custom_notifications", tags=["Custom Notifications"])


@router.post("/", response_class=JSONResponse)
async def create_notification(
    request: Request, current_user_id: int = Depends(tg_auth)
):
    data = await request.json()
    notification_data = CustomNotificationSchema.parse_obj(data)
    notification = await CustomNotificationService.create_notification(
        notification_data, current_user_id
    )
    return {"id": notification.id}


@router.put("/{notification_id}", response_class=JSONResponse)
async def update_notification(
    notification_id: int, 
    request: Request, 
    current_user_id: int = Depends(tg_auth)
):
    data = await request.json()
    notification_data = CustomNotificationSchema.parse_obj(data)
    await CustomNotificationService.update_notification(
        notification_id, notification_data, current_user_id
    )
    return {"message": "Notification updated"}


@router.delete("/{notification_id}", response_class=JSONResponse)
async def delete_notification(
    notification_id: int, current_user_id: int = Depends(tg_auth)
):
    await CustomNotificationService.delete_notification(notification_id, current_user_id)
    return {"message": "Notification deleted"}


@router.get("/group/{group_id}", response_class=JSONResponse)
async def get_group_notifications(
    group_id: int, current_user_id: int = Depends(tg_auth)
):
    notifications = await CustomNotificationService.get_group_notifications(
        group_id, current_user_id
    )
    return {"notifications": notifications}
