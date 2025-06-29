from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from mvp.core.db import get_async_session
from mvp.crud.task import (
    create_task, read_all_tasks_from_db, update_task, delete_task
)
from mvp.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from mvp.utils.for_tasks import (
    check_task_exists, admin_required, verify_executor_exists
)
from mvp.models.user import User
from mvp.core.user import current_user

router = APIRouter(prefix='/tasks', tags=['Tasks'])


@router.post(
        '/',
        response_model=TaskResponse,
        response_model_exclude_none=True,
)
async def create_new_task(
        task: TaskCreate,
        session: AsyncSession = Depends(get_async_session),
        cur_user: User = Depends(current_user),
):
    await verify_executor_exists(session, task.executor_id)
    await admin_required(cur_user)
    new_task = await create_task(task, session, cur_user)
    return new_task


@router.get(
    '/',
    response_model=list[TaskResponse],
    response_model_exclude_none=True,
)
async def get_all_tasks(
        session: AsyncSession = Depends(get_async_session),
):
    all_tasks = await read_all_tasks_from_db(session)
    return all_tasks


@router.patch(
    '/{task_id}',
    response_model=TaskResponse,
    response_model_exclude_none=True,
)
async def partially_update_task(
        task_id: int,
        obj_in: TaskUpdate,
        session: AsyncSession = Depends(get_async_session),
        cur_user: User = Depends(current_user),
):
    await verify_executor_exists(session, obj_in.executor_id)
    await admin_required(cur_user)
    task = await check_task_exists(
        task_id, session
    )
    task = await update_task(
        task, obj_in, session, cur_user
    )
    return task


@router.delete(
    '/{task_id}',
    response_model=TaskResponse,
    response_model_exclude_none=True,
)
async def remove_task(
        task_id: int,
        session: AsyncSession = Depends(get_async_session),
        cur_user: User = Depends(current_user),
):
    task = await admin_required(cur_user)
    task = await check_task_exists(
        task_id, session
    )
    task = await delete_task(
        task, session, cur_user
    )
    return task
