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

    @classmethod
    async def find_one_or_none(cls, **filter_by):

        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def add(cls, **values):

        async with async_session_maker() as session:
            async with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                except Exception as e:
                    await session.rollback()
                    raise e
                return new_instance

    @classmethod
    async def update(cls, filter, values):

        async with async_session_maker() as session:
            async with session.begin():
                instance = await cls.find_one_or_none(**filter)
                if not instance:
                    raise HTTPException(status_code=404, detail="Not Found")
                for var, value in values.items():
                    setattr(instance, var, value) if value else None

                session.add(instance)
                try:
                    await session.commit()
                except Exception as e:
                    await session.rollback()
                    raise e
                return instance

    @classmethod
    async def delete(cls, p_id):

        async with async_session_maker() as session:
            async with session.begin():
                hero = await session.get(cls.model, p_id)
                if not hero:
                    raise HTTPException(status_code=404, detail="Hero not found")
                await session.delete(hero)
                return {"ok": True}

===
Конец файла ===