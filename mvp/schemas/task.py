from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import date

from mvp.utils.status import Status


class TaskBase(BaseModel):
    name: str
    description: str
    deadline: date


class TaskCreate(TaskBase):
    status: Status = Status.OPEN


class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[date] = None
    status: Optional[Status] = None


class TaskResponse(TaskBase):
    id: int
    status: Status

    model_config = ConfigDict(from_attributes=True)
