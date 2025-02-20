from sqlalchemy import (
    String,
    BigInteger,
    Integer,
    Date,
    ForeignKey,
    Boolean,
    Table,
    Column,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

user_group_table = Table(
    "user_group_table",
    Base.metadata,
    Column("user_id", ForeignKey("users.telegram_id"), primary_key=True),
    Column("group_id", ForeignKey("groups.group_id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=True)
    birth_date: Mapped[Date] = mapped_column(Date, nullable=True)
    groups = relationship("Group", secondary=user_group_table, back_populates="users")
    notifications: Mapped[list["GroupNotification"]] = relationship(
        back_populates="for_user"
    )


class Group(Base):
    __tablename__ = "groups"

    group_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    group_name: Mapped[str] = mapped_column(String, nullable=False)
    base_text: Mapped[str] = mapped_column(String, nullable=True)
    notification_interval: Mapped[int] = mapped_column(Integer, default=1)
    admin_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.telegram_id"))

    notifications: Mapped[list["GroupNotification"]] = relationship(
        back_populates="group", cascade="all,delete"
    )
    users = relationship("User", secondary=user_group_table, back_populates="groups")


class GroupNotification(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    for_user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.telegram_id")
    )
    group_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("groups.group_id", ondelete="CASCADE")
    )
    for_user = relationship("User", back_populates="notifications")
    group = relationship("Group", back_populates="notifications")
