
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/custom_notifications/", response_class=HTMLResponse)
async def render_custom_notifications(request: Request):
    return templates.TemplateResponse("custom_notifications.html", {"request": request})
