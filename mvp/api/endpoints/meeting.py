from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from mvp.core.db import get_async_session
from mvp.core.user import current_user
from mvp.crud.meeting import create_meeting, delete_meeting, get_user_meetings
from mvp.models.user import User
from mvp.schemas.meeting import MeetingCreate, MeetingResponse

router = APIRouter(
    prefix="/meetings",
    tags=["Meetings"]
)


@router.post(
        "/",
        response_model=MeetingResponse
)
async def create_new_meeting(
    meeting_data: MeetingCreate,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user),
) -> MeetingResponse:
    if current_user.id not in meeting_data.participant_ids:
        meeting_data.participant_ids.append(current_user.id)

    new_meeting = await create_meeting(meeting_data, session)
    return new_meeting


@router.get("/", response_model=list[MeetingResponse])
async def get_my_meetings(
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user),
) -> list[MeetingResponse]:
    """
    Получить список встреч текущего пользователя
    """
    meetings = await get_user_meetings(
        user_id=current_user.id,
        session=session
    )
    return meetings


@router.delete("/{meeting_id}")
async def del_meeting(
    meeting_id: int,
    session: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(current_user),
) -> dict:
    return await delete_meeting(
        meeting_id=meeting_id,
        session=session
    )
