```python
from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse


router = APIRouter(prefix="", tags=["Фронтенд"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/custom-notifications", response_class=HTMLResponse)
async def custom_notifications_page(
    request: Request, 
    group_id: int = None, 
    user_id: int = None
):
    return templates.TemplateResponse(
        "custom_notifications.html",
        {
            "request": request,
            "group_id": group_id,
            "user_id": user_id
        },
    )

# ... остальные существующие роуты ...
```
