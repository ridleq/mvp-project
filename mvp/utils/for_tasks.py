from typing import Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from mvp.core.user import current_user
from mvp.models.task import Task
from mvp.models.user import User
from mvp.utils.user_role import UserRole


async def get_task_by_id(
        task_id: int,
        session: AsyncSession,
) -> Optional[Task]:
    db_task = await session.get(Task, task_id)
    return db_task


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


async def admin_required(
    cur_user: User = Depends(current_user),
) -> User:
    if cur_user.role != UserRole.TEAM_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только руководитель может выполнять это действие"
        )
    return cur_user


async def verify_executor_exists(
    session: AsyncSession,
    executor_id: Optional[int]
) -> None:
    user = await session.get(User, executor_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"Пользователь с ID {executor_id} не найден"
        )
