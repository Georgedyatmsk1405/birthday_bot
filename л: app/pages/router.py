```
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse


router = APIRouter(prefix="", tags=["Фронтенд"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "title": "Birthday Management"}
    )


@router.get("/user_form", response_class=HTMLResponse)
async def create_form(request: Request, user_id: int = None, user_name: str = None):
    return templates.TemplateResponse(
        "user_form.html",
        {
            "request": request,
            "user_id": user_id,
            "first_name": user_name,
        },
    )


@router.get("/form_group", response_class=HTMLResponse)
async def create_group(request: Request, user_id: int = None):
    return templates.TemplateResponse(
        "form_group.html",
        {
            "request": request,
            "user_id": user_id,
        },
    )


@router.get("/groups", response_class=HTMLResponse)
async def get_groups(request: Request):
    data_page = {
        "request": request,
        "access": False,
        "title_h1": "Мои подписки на группы",
    }
    return templates.TemplateResponse("groups.html", data_page)


@router.get("/admin_groups", response_class=HTMLResponse)
async def get_admin_groups(request: Request):
    data_page = {
        "request": request,
        "access": False,
        "title_h1": "Мои администрируемые группы",
    }
    return templates.TemplateResponse("admin_groups.html", data_page)


@router.get("/group_users", response_class=HTMLResponse)
async def get_group_users(request: Request, user_id: int = None, group_id: int = None):
    data_page = {"request": request, "access": False, "title_h1": "Пользователи группы"}
    return templates.TemplateResponse("group_users.html", data_page)


@router.get("/custom_notifications", response_class=HTMLResponse)
async def get_custom_notifications(request: Request, user_id: int = None, group_id: int = None):
    data_page = {
        "request": request,
        "user_id": user_id,
        "group_id": group_id,
        "title_h1": "Кастомные уведомления"
    }
    return templates.TemplateResponse("custom_notifications.html", data_page)

```
