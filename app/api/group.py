from fastapi import APIRouter, HTTPException, Depends
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from uuid import uuid4

from app.bot.create_bot import bot
from app.bot.utils.auth import tg_auth
from app.bot.utils.hash import hash_value
from app.repository.group import GroupRepo
from app.repository.user import UserRepo
from app.service.base import get_list
from app.service.redis import redis
from app.service.group import GroupService

router = APIRouter(prefix="", tags=["API"])


@router.post("/group", response_class=JSONResponse)
async def create_group(request: Request, current_user_id=Depends(tg_auth)):
    data = await request.json()
    if current_user_id != int(data["user_id"]):
        raise HTTPException(status_code=401, detail="permission denial")
    user = await UserRepo.find_one_or_none(telegram_id=data["user_id"])
    if not user:
        raise HTTPException(status_code=404, detail="not user")

    # Добавление заявки в базу данных
    await GroupRepo.add(
        admin_id=user.telegram_id,
        group_name=data["name"],
        notification_interval=data["notification_interval"],
    )


@router.put("/group", response_class=JSONResponse)
async def update_group(request: Request, current_user_id=Depends(tg_auth)):
    await GroupService.update_group(request, current_user_id=current_user_id)
    return {"message": "success"}


@router.post("/group/invite/{group_id}", response_class=JSONResponse)
async def generate_invite_group(group_id, current_user_id=Depends(tg_auth)):
    group = await GroupRepo.find_one_or_none(group_id=group_id)
    if not group:
        raise HTTPException(status_code=404, detail="not found group")
    if current_user_id != group.admin_id:
        raise HTTPException(status_code=401, detail="permission denial")

    group_uuid = str(uuid4())
    group_link = group_uuid + str(group_id)
    hashed_value = hash_value(group_link)
    await redis.set(hashed_value, group_id)
    # redis set hashed_value: group_id time day
    await bot.send_message(group.admin_id, text=str(hashed_value))
    return {"token": hashed_value}


@router.get("/groups", response_class=JSONResponse)
async def get_groups(user_id: int = None, current_user_id=Depends(tg_auth)):
    message = "У вас нет групп"
    if current_user_id != user_id:
        raise HTTPException(status_code=401, detail="permission denial")
    return await get_list(
        user_id, GroupRepo.get_subscriptions, {"user_id": user_id}, message
    )


@router.get("/admin_groups", response_class=JSONResponse)
async def get_admin_groups(user_id: int = None, current_user_id=Depends(tg_auth)):
    message = "У вас нет администрируемых групп"
    if current_user_id != user_id:
        raise HTTPException(status_code=401, detail="permission denial")
    return await get_list(
        user_id, GroupRepo.get_admin_groups, {"user_id": user_id}, message
    )


@router.get("/group_users", response_class=JSONResponse)
async def get_group_users(
    user_id: int = None, group_id: int = None, current_user_id=Depends(tg_auth)
):
    message = "В группе пока нет пользователей"
    group = await GroupRepo.find_one_or_none(group_id=group_id)
    if current_user_id != group.admin_id:
        raise HTTPException(status_code=401, detail="permission denial")
    return await get_list(
        user_id, UserRepo.get_group_users, {"group_id": group_id}, message
    )


@router.delete("/admin_group/{group_id}", response_class=JSONResponse)
async def delete_group(group_id: int, current_user_id=Depends(tg_auth)):
    await GroupService.delete_group(group_id=group_id, current_user_id=current_user_id)
    return {"message": "success"}
