from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from mvp.models.team import Team


async def get_team_or_404(team_id: int, session: AsyncSession):
    team = await session.execute(
        select(Team)
        .where(Team.id == team_id)
        .options(selectinload(Team.members))
    )
    team = team.scalars().first()

    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    return team
