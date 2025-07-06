from fastapi import APIRouter, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from mvp.core.db import get_async_session
from mvp.models.user import User
from mvp.models.team import Team
from mvp.core.user import current_user

templates = Jinja2Templates(directory="mvp/templates")

router = APIRouter(prefix="/teams")


@router.get("/")
async def team_list(
    request: Request,
    session: AsyncSession = Depends(get_async_session)
):
    query = await session.execute(
        select(Team).options(selectinload(Team.members),
                             selectinload(Team.admin))
    )
    teams = query.scalars().all()
    return templates.TemplateResponse(
        "teams.html", {"request": request, "teams": teams}
    )


@router.post("/create")
async def team_create(
    request: Request,
    name: str = Form(...),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    new_team = Team(name=name, admin_id=user.id)
    new_team.members.append(user)
    session.add(new_team)
    await session.commit()
    return RedirectResponse("/teams", status_code=303)
