from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from pathlib import Path
import os

from mvp.core.db import get_async_session
from mvp.models.meeting import Meeting
from mvp.models.user import User
from mvp.core.user import current_user
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

router = APIRouter(prefix="/meetings", tags=["Meetings Web"])


@router.get("/")
async def meetings_page(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    q = await session.execute(
        select(Meeting)
        .options(selectinload(Meeting.participants))
        .join(Meeting.participants)
        .where(User.id == user.id)
        .distinct()
    )
    meetings = q.scalars().unique().all()
    return templates.TemplateResponse(
        "meetings.html", {
            "request": request, "meetings": meetings, "user": user
        }
    )


@router.post("/create")
async def meeting_create(
    request: Request,
    start_time: str = Form(...),
    end_time: str = Form(...),
    participant_ids: str = Form(""),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    start_dt = datetime.fromisoformat(start_time)
    end_dt = datetime.fromisoformat(end_time)
    ids = [int(i.strip()) for i in participant_ids.split(",") if i.strip().isdigit()]
    if user.id not in ids:
        ids.append(user.id)
    part_q = await session.execute(select(User).where(User.id.in_(ids)))
    participants = list(part_q.scalars())
    # Создаем встречу
    meeting = Meeting(start_time=start_dt, end_time=end_dt)
    meeting.participants.extend(participants)
    session.add(meeting)
    await session.commit()
    return RedirectResponse("/meetings", status_code=303)


@router.post("/{meeting_id}/delete")
async def meeting_delete(
    meeting_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    # Может быть стоит добавить доп.защиту — пользователь должен быть участником
    q = await session.execute(select(Meeting).where(Meeting.id == meeting_id).options(selectinload(Meeting.participants)))
    meeting = q.scalar_one_or_none()
    if meeting is None:
        return RedirectResponse("/meetings", status_code=303)
    session.delete(meeting)
    await session.commit()
    return RedirectResponse("/meetings", status_code=303)
