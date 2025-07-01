from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class TaskReviewCreate(BaseModel):
    task_id: int
    rating: int = Field(..., ge=1, le=5)


class TaskReviewResponse(TaskReviewCreate):
    id: int
    reviewer_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserAverageRating(BaseModel):
    user_id: int
    avg_rating: float
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
