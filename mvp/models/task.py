from sqlalchemy import Column, Date, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from mvp.core.db import Base
from mvp.utils.task_status import Status


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
    comments = relationship(
        "Comment",
        back_populates="task",
        cascade="all, delete-orphan"
    )
    reviews = relationship(
        "TaskReview",
        back_populates="task",
        cascade="all, delete-orphan"
    )


class Comment(Base):
    content = Column(Text, nullable=False)
    task_id = Column(Integer, ForeignKey("task.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    task = relationship("Task", back_populates="comments")
    author = relationship("User", back_populates="comments")
