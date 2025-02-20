from datetime import timedelta

from fastapi import HTTPException
from app.config import settings
from app.api.schemas import GroupUpdateSchema
from app.repository.group import GroupRepo
from app.repository.notification import GroupNotificationRepo
from app.repository.user import UserRepo
from app.service.scheduler import scheduler


class GroupService:
    @staticmethod
    async def update_group(request, current_user_id):
        data = await request.json()
        user = await UserRepo.find_one_or_none(telegram_id=data["user_id"])
        if current_user_id != int(data["user_id"]):
            raise HTTPException(status_code=401, detail="permission denial")
        if not user:
            raise HTTPException(status_code=404, detail="no user")
        new_data = GroupUpdateSchema.parse_obj(data)

        # Добавление заявки в базу данных
        await GroupRepo.update(
            filter={"group_id": new_data.group_id}, values=new_data.dict()
        )
        if new_data.notification_interval:
            notes = await GroupNotificationRepo.find_all(group_id=new_data.group_id)
            if notes:
                job_id_to_trigger_args = {}
                for note in notes:
                    job_id = f"G{note.id}"
                    date = note.for_user.birth_date - timedelta(
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
    async def delete_group(group_id, current_user_id):
        notes = await GroupNotificationRepo.find_all(group_id=group_id)
        group = await GroupRepo.find_one_or_none(group_id=group_id)
        if not group or group.admin_id != current_user_id:
            raise ValueError
        await GroupRepo.delete(group_id)
        if notes:
            job_ids = [f"G{note.id}" for note in notes]
            scheduler.remove_jobs(job_ids=job_ids)
