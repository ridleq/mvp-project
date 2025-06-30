from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from fastapi import HTTPException

from mvp.models.user import User
from mvp.models.meeting import Meeting
from mvp.schemas.meeting import MeetingCreate
from mvp.utils.for_meeting import check_meeting_conflicts


async def create_meeting(
        new_meeting: MeetingCreate,
        session: AsyncSession,
) -> Meeting:
    await check_meeting_conflicts(
        session=session,
        start_time=new_meeting.start_time,
        end_time=new_meeting.end_time,
        participant_ids=new_meeting.participant_ids,
    )

    participants = [
        User(id=user_id) for user_id in new_meeting.participant_ids
    ]
    if new_meeting.participant_ids:
        stmt = select(User).where(User.id.in_(new_meeting.participant_ids))
        result = await session.execute(stmt)
        participants = result.scalars().all()

    meeting_data = new_meeting.dict(exclude={"participant_ids"})
    db_meeting = Meeting(**meeting_data)
    db_meeting.participants = participants

    session.add(db_meeting)
    await session.commit()
    await session.refresh(db_meeting)
    return db_meeting


async def get_user_meetings(
    user_id: int,
    session: AsyncSession,
) -> list[Meeting]:
    stmt = (
        select(Meeting)
        .options(selectinload(Meeting.participants))
        .join(Meeting.participants)
        .where(User.id == user_id)
        .order_by(Meeting.start_time.desc())
    )

    result = await session.execute(stmt)
    meetings = result.scalars().all()
    return meetings


async def delete_meeting(
    meeting_id: int,
    session: AsyncSession,
) -> dict:
    stmt = select(Meeting).where(Meeting.id == meeting_id)
    result = await session.execute(stmt)
    meeting = result.scalar_one_or_none()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    await session.delete(meeting)
    await session.commit()
    return {"status": "success", "message": "Meeting deleted"}
