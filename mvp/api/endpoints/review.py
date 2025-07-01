from datetime import datetime
from fastapi import APIRouter, Depends
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from mvp.core.db import get_async_session
from mvp.core.user import current_user
from mvp.crud.review import create_review, get_average_rating, get_user_reviews
from mvp.models.user import User
from mvp.schemas.review import (TaskReviewCreate, TaskReviewResponse,
                                UserAverageRating)
from mvp.utils.for_tasks import admin_required, check_task_exists

router = APIRouter(tags=['Review'])


@router.post(
    '/review',
    response_model=TaskReviewResponse,
    response_model_exclude_none=True,
)
async def create_new_review(
    review: TaskReviewCreate,
    session: AsyncSession = Depends(get_async_session),
    cur_user: User = Depends(current_user),
):
    await admin_required(cur_user)
    await check_task_exists(session, review.task_id)

    new_review = await create_review(session, review, cur_user.id)
    return new_review


@router.get(
    '/users/{user_id}/reviews',
    response_model=list[TaskReviewResponse],
    response_model_exclude_none=True,
)
async def get_user_reviews_endpoint(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
    cur_user: User = Depends(current_user),
):
    await admin_required(cur_user)
    reviews = await get_user_reviews(session, user_id)
    return reviews


@router.get(
    '/users/{user_id}/average_rating',
    response_model=UserAverageRating,
    response_model_exclude_none=True,
)
async def get_user_average_rating(
    user_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    session: AsyncSession = Depends(get_async_session),
    cur_user: User = Depends(current_user),
):
    await admin_required(cur_user)
    avg_rating = await get_average_rating(
        session,
        user_id,
        start_date,
        end_date
    )

    return UserAverageRating(
        user_id=user_id,
        avg_rating=round(avg_rating, 2),
        start_date=start_date,
        end_date=end_date
    )
