from datetime import datetime
from typing import Optional
from sqlalchemy import func
from sqlalchemy.orm import Session

from mvp.models.review import TaskReview
from mvp.models.task import Task
from mvp.schemas.review import TaskReviewCreate


def create_review(db: Session, review: TaskReviewCreate, reviewer_id: int):
    db_review = TaskReview(**review.dict(), reviewer_id=reviewer_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def get_user_reviews(db: Session, user_id: int):
    return (
        db.query(TaskReview)
        .join(Task, Task.id == TaskReview.task_id)
        .filter(Task.executor_id == user_id)
        .all()
    )


def get_average_rating(
    db: Session,
    user_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    query = (
        db.query(func.avg(TaskReview.rating))
        .join(Task, Task.id == TaskReview.task_id)
        .filter(Task.executor_id == user_id)
    )
    if start_date:
        query = query.filter(TaskReview.created_at >= start_date)
    if end_date:
        query = query.filter(TaskReview.created_at <= end_date)

    return query.scalar() or 0.0
