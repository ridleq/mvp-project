from pydantic import BaseModel, ConfigDict, Field, field_validator
from datetime import datetime
from typing import List

from .user import UserRead


class MeetingBase(BaseModel):
    start_time: datetime
    end_time: datetime

    @field_validator('end_time')
    def check_time_range(cls, end_time, values):
        start_time = values.data['start_time']
        if start_time >= end_time:
            raise ValueError("Конец встречи должен быть позже начала")
        return end_time


class MeetingCreate(MeetingBase):
    participant_ids: List[int] = Field(default_factory=list)


class MeetingResponse(MeetingBase):
    id: int
    participant_ids: list[int]

    model_config = ConfigDict(from_attributes=True)


class MeetingUserResponse(BaseModel):
    id: int
    start_time: datetime
    end_time: datetime
    participants: List[UserRead]

    model_config = ConfigDict(from_attributes=True)
