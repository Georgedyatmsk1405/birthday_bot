
from fastapi import APIRouter, Body, Depends, Path
from app.service.custom_notification import CustomNotificationService
from app.bot.utils.auth import tg_auth

router = APIRouter(tags=["Custom Notifications"])

@router.post("/custom_notifications/")
async def create_custom_notification(
    group_id: int = Body(...),
    content: str = Body(...),
    current_user_id=Depends(tg_auth)
):
    return await CustomNotificationService.create_custom_notification(group_id=group_id, content=content)

@router.get("/custom_notifications/{group_id}")
async def get_custom_notifications_for_group(
    group_id: int = Path(...),
    current_user_id=Depends(tg_auth)
):
    return await CustomNotificationService.get_custom_notifications_for_group(group_id=group_id)
