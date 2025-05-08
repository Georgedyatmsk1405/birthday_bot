```python
import logging
from contextlib import asynccontextmanager


from app.api.router import router
from app.pages.router import router as page_router
from app.api.custom_notifications import router as custom_notifications_router
from app.bot.create_bot import bot, dp, stop_bot, start_bot
from app.bot.handlers.user_router import user_router

from app.config import settings
from aiogram.types import Update
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from app.service.scheduler import scheduler

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    logging.info("Starting bot setup...")
    dp.include_router(user_router)
    await start_bot()
    webhook_url = settings.get_webhook_url()
    await bot.set_webhook(
        url=webhook_url,
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True,
    )
    logging.info(f"Webhook set to {webhook_url}")
    yield
    logging.info("Shutting down bot...")
    await bot.delete_webhook()
    await stop_bot()
    logging.info("Webhook deleted")


app = FastAPI(lifespan=lifespan)
app.include_router(router)
app.include_router(custom_notifications_router)
app.include_router(page_router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.post("/webhook")
async def webhook(request: Request) -> None:
    logging.info("Received webhook request")
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
    logging.info("Update processed")
```
