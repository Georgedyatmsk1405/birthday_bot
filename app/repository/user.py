from sqlalchemy import select, delete, insert
from sqlalchemy.exc import SQLAlchemyError

from app.database import async_session_maker
from app.models import User, GroupNotification
from app.models.models import user_group_table
from app.repository.base import BaseRepo
from app.repository.group import GroupRepo


class UserRepo(BaseRepo):
    model = User

    @classmethod
    async def get_group_users(cls, group_id: int):

        async with async_session_maker() as session:

            query = select(user_group_table).filter_by(group_id=group_id)
            groups = await session.execute(query)
            user_ids = [i[0] for i in groups]
            users = await session.execute(
                select(cls.model).filter(User.telegram_id.in_(user_ids))
            )
            users_birthday = users.scalars().all()

            return [
                {
                    "user_id": p.telegram_id,
                    "url": f"api/user_groups/{p.telegram_id}/{group_id}",
                    "name": p.username,
                    "birth_date": p.birth_date,
                }
                for p in users_birthday
            ]

    @classmethod
    async def get_group_user(cls, user_id: int, group_id: int):

        async with async_session_maker() as session:
            query = select(user_group_table).filter_by(group_id=group_id, user_id=user_id)
            groups = await session.execute(query)
            return [i[0] for i in groups]


    @classmethod
    async def exclude_user(cls, user_id, group_id: int):
        async with async_session_maker() as session:

            async with session.begin():
                user = await UserRepo.find_one_or_none_flush(
                    telegram_id=user_id, session=session
                )
                group = await GroupRepo.find_one_or_none_flush(
                    group_id=group_id, session=session
                )
                if not group or not user:
                    raise ValueError
                statement = delete(user_group_table).where(
                    user_group_table.c.user_id == user_id,
                    user_group_table.c.group_id == group_id,
                )
                notification = (
                    await session.execute(
                        select(GroupNotification).filter_by(
                            for_user_id=user_id, group_id=group_id
                        )
                    )
                ).scalar_one_or_none()
                note_id = notification.id
                await session.delete(notification)
                try:
                    await session.execute(statement)
                    await session.commit()
                    return note_id

                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e

    @classmethod
    async def add_to_group(cls, user_id, group_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                user = await UserRepo.find_one_or_none_flush(
                    telegram_id=user_id, session=session
                )
                group = await GroupRepo.find_one_or_none_flush(
                    group_id=group_id, session=session
                )
                if not group or not user:
                    raise ValueError
                statement = user_group_table.insert().values(
                    user_id=user_id, group_id=group_id
                )
                notification_statement = insert(GroupNotification).values(
                    for_user_id=user_id, group_id=group_id
                )
                notification_statement = notification_statement.returning(
                    GroupNotification.id
                )
                try:
                    await session.execute(statement)
                    new_id = (await session.execute(notification_statement)).first()[0]
                    await session.commit()
                    return new_id

                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
