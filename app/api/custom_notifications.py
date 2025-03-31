
from fastapi import APIRouter, Body, Path, HTTPException
from app.service.custom_notifications import CustomNotificationsService

router = APIRouter(tags=["Custom Notifications"])


@router.post("/{group_id}/notifications/")
async def create_custom_notification(
    group_id: int = Path(...),
    title: str = Body(...),
    content: str = Body(...),
):
    return await CustomNotificationsService.create(title, content, group_id)


@router.get("/{group_id}/notifications/")
async def list_custom_notifications(group_id: int = Path(...)):
    return await CustomNotificationsService.list(group_id)


@router.get("/{group_id}/notifications/{notification_id}")
async def retrieve_custom_notification(
    group_id: int = Path(...), notification_id: int = Path(...)
):
    notification = await CustomNotificationsService.retrieve(notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification


@router.put("/{group_id}/notifications/{notification_id}")
async def update_custom_notification(
    group_id: int = Path(...),
    notification_id: int = Path(...),
    title: str = Body(...),
    content: str = Body(...),
):
    return await CustomNotificationsService.update(notification_id, title, content)


@router.delete("/{group_id}/notifications/{notification_id}")
async def delete_custom_notification(
    group_id: int = Path(...), notification_id: int = Path(...)
):
    return await CustomNotificationsService.delete(notification_id)
