from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from mvp.core.db import get_async_session
from mvp.schemas.task import CommentResponse, CommentCreate
from mvp.crud.comments import create_comment
from mvp.models.user import User
from mvp.core.user import current_user
from mvp.utils.for_tasks import check_task_exists
from mvp.utils.for_comments import (
    get_comments_by_task,
    verify_comment_exists,
    verify_comment_owner

)
router = APIRouter(
    prefix="/tasks/{task_id}/comments",
    tags=["Comments"]
)


@router.post(
    "/",
    response_model=CommentResponse,
    response_model_exclude_none=True,
)
async def create_new_comment(
    task_id: int,
    comment: CommentCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user),
):
    new_comment = await check_task_exists(
        task_id, session
    )
    new_comment = await create_comment(
        task_id, comment, session, current_user
    )
    return new_comment


@router.get(
    "/",
    response_model=list[CommentResponse],
    response_model_exclude_none=True,
)
async def read_comments(
    task_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    comments = await get_comments_by_task(task_id, session)
    return comments


@router.delete(
    "/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_comment_endpoint(
    comment_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user),
):
    comment = await verify_comment_exists(comment_id, session)
    await verify_comment_owner(comment, current_user)
    await session.delete(comment)
    await session.commit()
