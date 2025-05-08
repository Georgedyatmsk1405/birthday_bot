```python
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, validator, Field


class CustomNotificationSchema(BaseModel):
    title: str
    content: str
    group_id: int
    created_by: int
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        orm_mode = True
```
