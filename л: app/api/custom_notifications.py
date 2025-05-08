```python
from fastapi import APIRouter, HTTPException, Depends
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from app.bot.utils.auth import tg_auth
from app.repository.custom_notification import CustomNotificationRepo
from app.service.custom_notification import CustomNotificationService
from app.api.schemas import CustomNotificationSchema

router = APIRouter(prefix="/custom_notifications", tags=["Custom Notifications"])


@router.post("", response_class=JSONResponse)
async def create_custom_notification(
    request: Request, current_user_id=Depends(tg_auth)
):
    data = await request.json()
    if current_user_id != int(data["user_id"]):
        raise HTTPException(status_code=401, detail="Permission denied")
    await CustomNotificationService.create_custom_notification(data)
    return {"message": "Success"}


@router.get("/{notification_id}", response_class=JSONResponse)
async def get_custom_notification(
    notification_id: int, current_user_id=Depends(tg_auth)
):
    notification = await CustomNotificationRepo.find_one_or_none(id=notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Not found")
    if current_user_id != notification.created_by:
        raise HTTPException(status_code=401, detail="Permission denied")
    return notification


@router.put("/{notification_id}", response_class=JSONResponse)
async def update_custom_notification(
    notification_id: int, request: Request, current_user_id=Depends(tg_auth)
):
    data = await request.json()
    if current_user_id != int(data["user_id"]):
        raise HTTPException(status_code=401, detail="Permission denied")
    await CustomNotificationService.update_custom_notification(notification_id, data)
    return {"message": "Success"}


@router.delete("/{notification_id}", response_class=JSONResponse)
async def delete_custom_notification(
    notification_id: int, current_user_id=Depends(tg_auth)
):
    notification = await CustomNotificationRepo.find_one_or_none(id=notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Not found")
    if current_user_id != notification.created_by:
        raise HTTPException(status_code=401, detail="Permission denied")
    await CustomNotificationService.delete_custom_notification(notification_id)
    return {"message": "Success"}
```
