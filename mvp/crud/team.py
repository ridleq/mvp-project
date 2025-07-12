from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from mvp.models.team import Team
from mvp.models.user import User
from mvp.schemas.team import TeamCreate


async def team_create(
        session: AsyncSession,
        obj_in: TeamCreate,
        admin: User
) -> Team:
    try:
        team = Team(name=obj_in.name, admin_id=admin.id)

        if obj_in.user_ids:
            users = await session.execute(
                select(User).where(User.id.in_(obj_in.user_ids))
            )
            for user in users.scalars():
                team.members.append(user)

        session.add(team)
        await session.commit()
        await session.refresh(team)
        result = await session.execute(
            select(Team).options(
                joinedload(Team.members)
            ).where(Team.id == team.id)
        )
        team = result.scalar_one()
        return team

    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=400,
            detail="Team with such name already exists"
        )
