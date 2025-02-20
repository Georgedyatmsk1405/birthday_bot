from aiogram.fsm.state import StatesGroup, State


class User(StatesGroup):
    group_id = State()
    for_user_id = State()
