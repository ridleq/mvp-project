from sqlalchemy import (
    Column, Integer, ForeignKey, DateTime
)
from sqlalchemy.orm import relationship
from datetime import datetime

from mvp.core.db import Base


class TaskReview(Base):
    task_id = Column(Integer, ForeignKey("task.id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    task = relationship("Task", back_populates="reviews")
    reviewer = relationship("User")
