from fastapi import APIRouter

from .group import router as group_router
from .user import router as user_router
from .notification import router as notification_router

router = APIRouter(prefix="/api", tags=["API"])
router.include_router(group_router)
router.include_router(user_router)
router.include_router(notification_router)

===
Конец файла ===