from fastapi import APIRouter, Depends, HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from app.bot.utils.auth import tg_auth
from app.repository.group import GroupRepo
from app.service.user import UserService

router = APIRouter(prefix="", tags=["API"])


@router.delete("/user_groups/{user_id}/{group_id}", response_class=JSONResponse)
async def exclude_user(user_id: int, group_id: int, current_user_id=Depends(tg_auth)):
    group = await GroupRepo.find_one_or_none(group_id=group_id)
    if current_user_id not in (group.admin_id, user_id):
        raise HTTPException(status_code=401, detail="permission denial")
    await UserService.exclude_user(user_id, group_id)

    return {"message": "success!"}


@router.put("/users/{user_id}", response_class=JSONResponse)
async def update_user(request: Request, user_id: int, current_user_id=Depends(tg_auth)):
    if current_user_id != user_id:
        raise HTTPException(status_code=401, detail="permission denial")
    await UserService.update_user(request, user_id)

    return {"message": "success!"}

@router.post("/custom_notifications", response_class=JSONResponse)
async def create_custom_notification(request: Request, current_user_id=Depends(tg_auth)):
    data = await request.json()
    schema = CustomNotificationSchema.parse_obj(data)
    await GroupNotificationRepo.add(content=schema.content, for_user_id=schema.for_user_id, group_id=schema.group_id)
    return {"message": "Custom Notification Created Successfully"}

@router.get("/custom_notifications", response_class=JSONResponse)
async def list_custom_notifications(current_user_id=Depends(tg_auth)):
    notifications = await GroupNotificationRepo.find_all()
    return {"notifications": notifications}

@router.get("/custom_notifications/{notification_id}", response_class=JSONResponse)
async def retrieve_custom_notification(notification_id: int, current_user_id=Depends(tg_auth)):
    notification = await GroupNotificationRepo.find_one_or_none(id=notification_id)
    if not notification:
        raise HTTPException(status_code=404, detail="Custom Notification Not Found")
    return {"notification": notification}

@router.put("/custom_notifications/{notification_id}", response_class=JSONResponse)
async def update_custom_notification(request: Request, notification_id: int, current_user_id=Depends(tg_auth)):
    data = await request.json()
    schema = CustomNotificationSchema.parse_obj(data)
    await GroupNotificationRepo.update(filter={"id": notification_id}, values=schema.dict())
    return {"message": "Custom Notification Updated Successfully"}

@router.delete("/custom_notifications/{notification_id}", response_class=JSONResponse)
async def delete_custom_notification(notification_id: int, current_user_id=Depends(tg_auth)):
    await GroupNotificationRepo.delete(p_id=notification_id)
    return {"message": "Custom Notification Deleted Successfully"}

===
Конец файла ===