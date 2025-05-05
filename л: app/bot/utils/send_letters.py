```
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
        
        # Получаем активные кастомные уведомления для группы
        custom_notifications = await session.execute(
            select(CustomNotification)
            .filter_by(group_id=g.group_id, is_active=True)
        )
        custom_messages = "\n\n".join(
            [n.message for n in custom_notifications.scalars()]
        )
        
        full_message = (
            f"{g.for_user.birth_date} Отмечает день рождения {g.for_user.username}\n"
            f"Для поздравления используйте команду send_letter-{note_id}"
        )
        
        if custom_messages:
            full_message = f"{custom_messages}\n\n{full_message}"
            
    await bot.send_message(chat_id=admin_id, text=full_message)


async def send_text(user_id, message):
    await bot.send_message(user_id, text=message.text)


async def send_photo(user_id, message):
    await bot.send_photo(
        chat_id=user_id, photo=message.photo[-1].file_id, caption=message.text
    )
