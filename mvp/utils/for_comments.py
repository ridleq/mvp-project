from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from mvp.models.task import Comment
from mvp.models.user import User


async def get_comments_by_task(
    task_id: int,
    session: AsyncSession
) -> list[Comment]:
    query = (
        select(Comment)
        .options(joinedload(Comment.author))
        .where(Comment.task_id == task_id)
    )
    result = await session.execute(query)
    return result.scalars().unique().all()


async def verify_comment_exists(
    comment_id: int,
    session: AsyncSession
) -> Comment:
    comment = await session.get(Comment, comment_id)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Комментарий не найден"
        )
    return comment


async def verify_comment_owner(
    comment: Comment,
    current_user: User
) -> None:
    if comment.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав"
        )
