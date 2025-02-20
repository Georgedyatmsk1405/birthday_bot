from sqlalchemy import select

from app.database import async_session_maker
from app.models import Group
from app.models.models import user_group_table
from app.repository.base import BaseRepo


class GroupRepo(BaseRepo):
    model = Group

    @classmethod
    async def get_subscriptions(cls, user_id: int):

        async with async_session_maker() as session:

            query = select(user_group_table).filter_by(user_id=user_id)
            groups = await session.execute(query)
            group_ids = [i[1] for i in groups]
            groups = await session.execute(
                select(cls.model).filter(Group.group_id.in_(group_ids))
            )
            personal_applications = groups.scalars().all()

            return [
                {
                    "url": f"api/user_groups/{user_id}/{p.group_id}",
                    "name": p.group_name,  # Название услуги
                }
                for p in personal_applications
            ]

    @classmethod
    async def get_admin_groups(cls, user_id: int):

        groups = await super().find_all(admin_id=user_id)

        return [
            {
                "url": f"api/admin_group/{g.group_id}",
                "name": g.group_name,
                "get_url": f"group_users?group_id={g.group_id}&user_id={user_id}",
            }
            for g in groups
        ]
