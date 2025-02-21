from datetime import timedelta
from app.config import settings
from app.api.schemas import UserSchema
from app.repository.group import GroupRepo
from app.repository.notification import GroupNotificationRepo
from app.repository.user import UserRepo
from app.service.redis import redis
from app.service.scheduler import scheduler
from app.bot.utils.send_letters import send_to_admin_user_notification


class UserService:

    @staticmethod
    async def add_user_to_group(user_id, token):
        user = await UserRepo.find_one_or_none(telegram_id=user_id)
        group_id = await redis.get(token)
        if not group_id:
            raise ValueError("Expired")
        if not user.birth_date:
            return "Для вступления в группу заполните Дату рождения"
        if not user.username:
            return "Для вступления в группу заполните имя"
        group = await GroupRepo.find_one_or_none(group_id=group_id)
        date = user.birth_date - timedelta(days=group.notification_interval)
        exist = await UserRepo.get_group_user(user_id=user_id, group_id=group_id)
        if exist:
            return "Вы уже вступили"
        note_id = await UserRepo.add_to_group(user_id=user_id, group_id=group_id)
        job_id = f"G{note_id}"
        scheduler.add_job(
            send_to_admin_user_notification,
            "cron",
            id=job_id,
            day=date.day,
            month=date.month,
            hour=settings.HOUR,
            minute=settings.MINUTE,
            jitter=1,
            kwargs={
                "note_id": note_id,
            },
        )
        return "Вы успешно вступили в группу"

    @staticmethod
    async def update_user(request, user_id):
        data = await request.json()
        user = await UserRepo.find_one_or_none(telegram_id=user_id)
        if not user:
            raise ValueError("no user")
        user_data = UserSchema.parse_obj(data)
        user_id = user_id
        notes = await GroupNotificationRepo.find_all(for_user_id=user_id)
        await UserRepo.update(filter={"telegram_id": user_id}, values=user_data.dict())
        if notes:
            job_id_to_trigger_args = {}
            for note in notes:
                job_id = f"G{note.id}"
                date = user_data.birth_date - timedelta(
                    days=note.group.notification_interval
                )
                job_id_to_trigger_args[job_id] = {
                    "day": date.day,
                    "month": date.month,
                    "hour": settings.HOUR,
                    "minute": settings.MINUTE,
                }
            scheduler.reschedule_jobs(job_id_to_trigger_args)

    @staticmethod
    async def exclude_user(user_id, group_id):
        note_id = await UserRepo.exclude_user(user_id, group_id)
        job_id = f"G{note_id}"
        scheduler.remove_job(job_id=job_id)
