from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict

from mvp.utils.task_status import Status


class TaskBase(BaseModel):
    name: str
    description: str
    deadline: date
    executor_id: Optional[int] = None


class TaskCreate(TaskBase):
    status: Status = Status.OPEN


class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[date] = None
    status: Optional[Status] = None
    executor_id: Optional[int] = None


class TaskResponse(TaskBase):
    id: int
    status: Status

    model_config = ConfigDict(from_attributes=True)


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    pass


class CommentResponse(CommentBase):
    id: int
    author_id: int
    task_id: int

    model_config = ConfigDict(from_attributes=True)
