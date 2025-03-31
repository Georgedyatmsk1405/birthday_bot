
from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class CustomNotification(Base):
    __tablename__ = "custom_notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    group_id = Column(Integer, ForeignKey("groups.group_id"))
    
    group = relationship("Group", backref="custom_notifications")
