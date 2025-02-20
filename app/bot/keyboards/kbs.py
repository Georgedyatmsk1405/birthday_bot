from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.config import settings


def main_keyboard(user_id: int):
    kb = InlineKeyboardBuilder()
    url_admin_groups = f"{settings.BASE_SITE}/admin_groups?user_id={user_id}"
    url_subscriptions = f"{settings.BASE_SITE}/groups?user_id={user_id}"
    url_create_group = f"{settings.BASE_SITE}/form_group?user_id={user_id}"
    url_update_user = f"{settings.BASE_SITE}/user_form?user_id={user_id}"
    kb.button(
        text="📝 Администрируемые группы", web_app=WebAppInfo(url=url_admin_groups)
    )
    kb.button(
        text="📝Мои подписки на группы", web_app=WebAppInfo(url=url_subscriptions)
    )
    kb.button(text="📝 Создать группу", web_app=WebAppInfo(url=url_create_group))
    kb.button(text="📝 Редактировать профиль", web_app=WebAppInfo(url=url_update_user))

    kb.adjust(1)
    return kb.as_markup()
