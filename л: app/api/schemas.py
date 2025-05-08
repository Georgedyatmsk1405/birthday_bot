```python
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import date


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


class CustomNotificationCreate(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    group_id: int


class CustomNotificationUpdate(BaseModel):
    message: Optional[str] = Field(None, min_length=1, max_length=1000)
    is_active: Optional[bool] = None


class CustomNotificationResponse(BaseModel):
    id: int
    message: str
    is_active: bool
    created_at: datetime
    group_id: int
```
