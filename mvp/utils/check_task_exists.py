from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from mvp.models.task import Task
from mvp.utils.get_task_id import get_task_by_id


async def check_task_exists(
        task_id: int,
        session: AsyncSession,
) -> Task:
    task = await get_task_by_id(
        task_id, session
    )
    if task is None:
        raise HTTPException(
            status_code=404,
            detail='Задача не найдена!'
        )
    return task
