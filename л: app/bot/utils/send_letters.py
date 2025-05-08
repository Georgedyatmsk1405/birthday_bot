```python
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.bot.create_bot import bot
from app.database import async_session_maker
from app.models.models import GroupNotification, CustomNotification


async def send_to_admin_user_notification(note_id=None):
    async with async_session_maker() as session:
        query = (
            select(GroupNotification)
            .filter_by(id=note_id)
            .options(
                selectinload(GroupNotification.group),
                selectinload(GroupNotification.for_user),
            )
        )
        result = await session.execute(query)
        g = result.scalar_one_or_none()
        admin_id = g.group.admin_id
    await bot.send_message(
        chat_id=admin_id,
        text=f"{g.for_user.birth_date} Отмечает день рождения {g.for_user.username} для поздравления используйте команду send_letter-{note_id}",
    )


async def send_group_notifications(group_id: int, message: str):
    async with async_session_maker() as session:
        query = select(CustomNotification).filter_by(
            group_id=group_id, 
            is_active=True
        )
        result = await session.execute(query)
        notifications = result.scalars().all()
        
        for notification in notifications:
            await bot.send_message(
                chat_id=group_id,
                text=notification.message
            )


async def send_text(user_id, message):
    await bot.send_message(user_id, text=message.text)


async def send_photo(user_id, message):
    await bot.send_photo(
        chat_id=user_id, 
        photo=message.photo[-1].file_id, 
        caption=message.text
    )
```
