from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from mvp.models.task import Task
from mvp.models.user import User
from mvp.schemas.task import TaskCreate, TaskUpdate


async def create_task(
        new_task: TaskCreate,
        session: AsyncSession,
        current_user: User,
) -> Task:
    new_task_data = new_task.dict()

    db_task = Task(**new_task_data)

    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)
    return db_task


async def read_all_tasks_from_db(
        session: AsyncSession,
) -> list[Task]:
    db_task = await session.execute(select(Task))
    return db_task.scalars().all()


async def update_task(
        db_task: Task,
        task_in: TaskUpdate,
        session: AsyncSession,
        current_user: User,
) -> Task:
    update_data = task_in.dict(exclude_unset=True, exclude={"executor_id"})

    for field, value in update_data.items():
        setattr(db_task, field, value)
    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)
    return db_task


async def delete_task(
        db_task: Task,
        session: AsyncSession,
        current_user: User,
) -> Task:
    await session.delete(db_task)
    await session.commit()
    return db_task
