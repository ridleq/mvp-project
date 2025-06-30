from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from mvp.models.user import User
from mvp.models.team import Team
from mvp.schemas.team import TeamCreate


async def team_create(
        session: AsyncSession,
        obj_in: TeamCreate,
        admin: User
) -> Team:
    team = Team(name=obj_in.name, admin_id=admin.id)

    team = Team(name=obj_in.name, admin_id=admin.id)

    if obj_in.user_ids:
        users = await session.execute(
            select(User).where(User.id.in_(obj_in.user_ids))
        )
        for user in users.scalars():
            if user not in team.members:
                team.members.append(user)

    session.add(team)
    await session.commit()
    await session.refresh(team)
    return team
