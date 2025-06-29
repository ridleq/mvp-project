from sqlalchemy.ext.asyncio import AsyncSession

from mvp.models.task import Comment
from mvp.models.user import User
from mvp.schemas.task import CommentCreate


async def create_comment(
    task_id: int,
    comment_data: CommentCreate,
    session: AsyncSession,
    current_user: User
) -> Comment:
    new_comment = Comment(
        content=comment_data.content,
        task_id=task_id,
        author_id=current_user.id
    )
    session.add(new_comment)
    await session.commit()
    await session.refresh(new_comment)
    return new_comment
