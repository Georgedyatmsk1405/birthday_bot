```
from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from app.bot.utils.auth import tg_auth
from app.repository.custom_notification import CustomNotificationRepo
from app.repository.group import GroupRepo
from app.api.schemas import (
    CustomNotificationCreateSchema,
    CustomNotificationUpdateSchema
)

router = APIRouter(prefix="/api/custom_notifications", tags=["Custom Notifications"])


@router.post("/", response_class=JSONResponse)
async def create_custom_notification(
    request: Request, 
    current_user_id=Depends(tg_auth)
):
    data = await request.json()
    schema = CustomNotificationCreateSchema.parse_obj(data)
    
    group = await GroupRepo.find_one_or_none(group_id=schema.group_id)
    if not group or group.admin_id != current_user_id:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    notification = await CustomNotificationRepo.add(
        group_id=schema.group_id,
        message=schema.message
    )
    
    return {"id": notification.id, "message": "Custom notification created"}


@router.get("/{group_id}", response_class=JSONResponse)
async def get_custom_notifications(
    group_id: int,
    current_user_id=Depends(tg_auth)
):
    group = await GroupRepo.find_one_or_none(group_id=group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    if group.admin_id != current_user_id:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    notifications = await CustomNotificationRepo.find_all_active(group_id=group_id)
    return [{
        "id": n.id,
        "message": n.message,
        "is_active": n.is_active,
        "created_at": n.created_at
    } for n in notifications]


@router.put("/{notification_id}", response_class=JSONResponse)
async def update_custom_notification(
    notification_id: int,
    request: Request,
    current_user_id=Depends(tg_auth)
):
    data = await request.json()
    schema = CustomNotificationUpdateSchema.parse_obj(data)
    
    notification = await CustomNotificationRepo.find_one_or_none(id=notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    group = await GroupRepo.find_one_or_none(group_id=notification.group_id)
    if not group or group.admin_id != current_user_id:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    update_data = schema.dict(exclude_unset=True)
    await CustomNotificationRepo.update(
        filter={"id": notification_id},
        values=update_data
    )
    
    return {"message": "Custom notification updated"}


@router.delete("/{notification_id}", response_class=JSONResponse)
async def delete_custom_notification(
    notification_id: int,
    current_user_id=Depends(tg_auth)
):
    notification = await CustomNotificationRepo.find_one_or_none(id=notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    group = await GroupRepo.find_one_or_none(group_id=notification.group_id)
    if not group or group.admin_id != current_user_id:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    await CustomNotificationRepo.delete(notification_id)
    return {"message": "Custom notification deleted"}

```
