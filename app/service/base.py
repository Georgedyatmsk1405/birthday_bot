from app.repository.user import UserRepo


async def get_list(user_id, func, kwargs, message):
    user_check = await UserRepo.find_one_or_none(telegram_id=user_id)
    if user_id is None or user_check is None:
        return {"not_found": "no user"}
    else:
        data = {}
        entities = await func(**kwargs)
        if len(entities):
            data["applications"] = entities
        else:
            data["message"] = message
        return data
