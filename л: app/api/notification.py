from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from app.bot.utils.auth import tg_auth
from app.service.notification import NotificationService
from app.api.schemas import NotificationSchema

router = APIRouter(prefix="/notification", tags=["Notifications"])


@router.post("/{group_id}", response_class=JSONResponse)
async def create_notification(
    request: Request, group_id: int, current_user_id=Depends(tg_auth)
):
    data = await request.json()
    schema = NotificationSchema.parse_obj(data)
    await NotificationService.create_notification(
        content=schema.content, group_id=group_id, for_user_id=current_user_id
    )
    return {"message": "success"}


@router.get("/{group_id}", response_class=JSONResponse)
async def list_notifications(group_id: int, current_user_id=Depends(tg_auth)):
    notifications = await NotificationService.list_notifications(group_id=group_id)
    return {"notifications": notifications}


@router.get("/{notification_id}", response_class=JSONResponse)
async def retrieve_notification(notification_id: int, current_user_id=Depends(tg_auth)):
    notification = await NotificationService.retrieve_notification(notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification Not Found")
    return {"notification": notification}


@router.put("/{notification_id}", response_class=JSONResponse)
async def update_notification(
    request: Request, notification_id: int, current_user_id=Depends(tg_auth)
):
    data = await request.json()
    schema = NotificationSchema.parse_obj(data)
    await NotificationService.update_notification(
        notification_id=notification_id, content=schema.content
    )
    return {"message": "success"}


@router.delete("/{notification_id}", response_class=JSONResponse)
async def delete_notification(notification_id: int, current_user_id=Depends(tg_auth)):
    await NotificationService.delete_notification(notification_id=notification_id)
    return {"message": "success"}

===
Конец файла ===