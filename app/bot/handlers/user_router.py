import asyncio


from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from app.bot.create_bot import dp
from app.bot.utils.send_letters import send_photo, send_text
from app.repository.notification import GroupNotificationRepo
from app.repository.user import UserRepo

from app.bot.utils.utils import greet_user
from app.service.user import UserService

user_router = Router()


class User(StatesGroup):
    group_id = State()
    for_user_id = State()


class Invite(StatesGroup):
    inv = State()


@user_router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """
    Обрабатывает команду /start.
    """
    user = await UserRepo.find_one_or_none(telegram_id=message.from_user.id)
    if not user:
        await UserRepo.add(
            telegram_id=message.from_user.id, username=message.from_user.username
        )
    await greet_user(message, is_new_user=not user)


@user_router.message(F.text == "🔙 Назад")
async def cmd_back_home(message: Message) -> None:
    """
    Обрабатывает нажатие кнопки "Назад".
    """
    await greet_user(message, is_new_user=False)


@user_router.message(F.text.contains("send_letter"))
async def init_admin_message(message: Message, state: FSMContext):
    note_id = message.text.strip().split("-")[1]
    note = await GroupNotificationRepo.find_one_or_none(id=note_id)
    await state.set_state(User.group_id)  # update state user id group id
    await state.update_data(group_id=note.group_id, for_user_id=note.for_user_id)
    await message.answer("Введите сообщение для группы, для отмены введите stop")


@dp.message(User.group_id)
async def send_from_admin_to_group(message: Message, state: FSMContext):
    if message.text.strip() == "stop":
        await state.clear()
        await message.answer("Отправка остановлена")
        return
    data = await state.get_data()
    user_id, group_id = data["for_user_id"], data["group_id"]
    user_ids = [u["user_id"] for u in await UserRepo.get_group_users(group_id=group_id)]
    tasks = []
    print(user_ids)
    if message.text is not None:
        for user_id in user_ids:
            tasks.append(send_text(user_id, message))
    elif message.photo is not None:
        for user_id in user_ids:
            tasks.append(send_photo(user_id, message))
    await asyncio.gather(*tasks)
    await state.clear()
    await message.answer("Сообщение отправлено")


@user_router.message(F.text.contains("enter"))
async def invite_start(message: Message, state: FSMContext):
    await state.set_state(Invite.inv)  # update state user id group id
    await message.answer("Введите токен")


@dp.message(Invite.inv)
async def add_group_user(message: Message, state: FSMContext):
    token = message.text.strip()
    user_id = message.from_user.id
    result = await UserService.add_user_to_group(token=token, user_id=user_id)
    await state.clear()
    await message.answer(result)
