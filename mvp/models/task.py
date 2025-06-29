from sqlalchemy import (
    Column, Date, String, Text, Enum, Integer, ForeignKey
)
from sqlalchemy.orm import relationship

from mvp.core.db import Base
from mvp.utils.status import Status


class Task(Base):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    deadline = Column(Date)
    status = Column(
        Enum(Status),
        default=Status.OPEN,
        nullable=False
    )
    executor_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    executor = relationship("User", back_populates="tasks")
