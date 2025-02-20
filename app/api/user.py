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
