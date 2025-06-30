from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from mvp.core.db import get_async_session
from mvp.crud.team import team_create
from mvp.schemas.team import (
    TeamCreate, TeamBase, TeamMembersResponse, TeamUpdate
)
from mvp.utils.for_tasks import admin_required
from mvp.models.user import User
from mvp.core.user import current_user
from mvp.models.team import Team
from mvp.utils.for_team import get_team_or_404


router = APIRouter(prefix='/team', tags=['Team'])


@router.post(
        "/",
        response_model=TeamBase,
)
async def create_team(
    team_in: TeamCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    team = await admin_required(user)
    team = await team_create(
        session=session,
        obj_in=team_in,
        admin=user
    )
    return team


@router.get(
    "/{team_id}",
    response_model=TeamMembersResponse,
)
async def read_team_members(
    team_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    team = await get_team_or_404(team_id, session)
    member_ids = [member.id for member in team.members]

    return TeamMembersResponse(
        team_id=team_id,
        members=member_ids
    )


@router.patch(
    "/{team_id}",
    response_model=TeamBase,
)
async def update_team(
    team_id: int,
    team_update: TeamUpdate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    team = await session.execute(
        select(Team)
        .where(Team.id == team_id)
        .options(selectinload(Team.members))
    )
    team = team.scalars().first()
    await get_team_or_404(team_id, session)
    await admin_required(user)
    team.name = team_update.name
    if team_update.add:
        for user_id in team_update.add:
            if not any(member.id == user_id for member in team.members):
                user_to_add = await session.execute(
                    select(User).where(User.id == user_id)
                )
                user_to_add = user_to_add.scalars().first()
                if user_to_add:
                    team.members.append(user_to_add)

    if team_update.remove:
        for user_id in team_update.remove:
            user_to_remove = next(
                (member for member in team.members if member.id == user_id),
                None
            )
            if user_to_remove:
                team.members.remove(user_to_remove)

    session.add(team)
    await session.commit()
    await session.refresh(team)

    return team
