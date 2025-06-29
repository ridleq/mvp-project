from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from mvp.models.task import Task


async def get_task_by_id(
        task_id: int,
        session: AsyncSession,
) -> Optional[Task]:
    db_task = await session.get(Task, task_id)
    return db_task
