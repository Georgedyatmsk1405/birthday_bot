```python
from sqlalchemy import (
    String,
    Text,
    Integer,
    BigInteger,
    Column,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class CustomNotification(Base):
    __tablename__ = "custom_notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey("groups.group_id"))
    created_by: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.telegram_id"))
    created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    group = relationship("Group", backref="custom_notifications")
    creator = relationship("User", foreign_keys=[created_by])
```
