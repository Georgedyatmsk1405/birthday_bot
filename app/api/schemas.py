from typing import Optional

from pydantic import BaseModel, Field
from datetime import date


# Модель для валидации данных
class PersonalNotificationData(BaseModel):
    birth_date: date
    user_id: int
    name: str = Field(..., min_length=2, max_length=50, description="Пол клиента")
    initData: str


class GroupUpdateSchema(BaseModel):
    group_name: str
    group_id: int
    notification_interval: Optional[int] = None

    class Config:
        extra = "ignore"


class UserSchema(BaseModel):
    birth_date: date
    username: Optional[str] = None

    class Config:
        extra = "ignore"
