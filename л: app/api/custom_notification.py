```python
from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from app.bot.utils.auth import tg_auth
from app.service.custom_notification import CustomNotificationService
from app.api.schemas import CustomNotificationCreateSchema, CustomNotificationUpdateSchema


router = APIRouter(prefix="/api/custom-notifications", tags=["Custom Notifications"])


@router.post("", response_class=JSONResponse)
async def create_notification(
    request: Request, 
    current_user_id: int = Depends(tg_auth)
):
    data = await request.json()
    validated_data = CustomNotificationCreateSchema.parse_obj(data)
    return await CustomNotificationService.create_notification(
        validated_data, current_user_id
    )


@router.put("/{notification_id}", response_class=JSONResponse)
async def update_notification(
    notification_id: int,
    request: Request,
    current_user_id: int = Depends(tg_auth)
):
    data = await request.json()
    validated_data = CustomNotificationUpdateSchema.parse_obj(data)
    return await CustomNotificationService.update_notification(
        notification_id, validated_data, current_user_id
    )


@router.delete("/{notification_id}", response_class=JSONResponse)
async def delete_notification(
    notification_id: int,
    current_user_id: int = Depends(tg_auth)
):
    return await CustomNotificationService.delete_notification(
        notification_id, current_user_id
    )


@router.get("/group/{group_id}", response_class=JSONResponse)
async def get_group_notifications(
    group_id: int,
    current_user_id: int = Depends(tg_auth)
):
    group = await GroupRepo.find_one_or_none(group_id=group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    if current_user_id != group.admin_id:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    return await CustomNotificationService.get_group_notifications(group_id)
```
