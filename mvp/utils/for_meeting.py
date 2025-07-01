from datetime import datetime
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from mvp.models.meeting import Meeting
from mvp.models.user import User


async def check_meeting_conflicts(
    session: AsyncSession,
    start_time: datetime,
    end_time: datetime,
    participant_ids: list[int],
    exclude_meeting_id: Optional[int] = None
) -> None:
    if not participant_ids:
        return

    if start_time >= end_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Конец встречи должен быть позже начала"
        )

    query = (
        select(Meeting)
        .join(Meeting.participants)
        .where(
            and_(
                User.id.in_(participant_ids),
                or_(
                    and_(
                        Meeting.start_time < end_time,
                        Meeting.end_time > start_time
                    ),
                    Meeting.start_time == start_time
                )
            )
        )
    )

    if exclude_meeting_id is not None:
        query = query.where(Meeting.id != exclude_meeting_id)

    result = await session.execute(query)
    conflicts = result.scalars().all()

    if conflicts:
        conflict_ids = sorted({m.id for m in conflicts})
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Обнаружены пересекающиеся встречи: ID {conflict_ids}"
        )
