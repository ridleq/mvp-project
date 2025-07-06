from fastapi import Request, APIRouter
from fastapi.templating import Jinja2Templates
from pathlib import Path
import os

from mvp.core.user import fastapi_users

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

current_user_optional = fastapi_users.current_user(optional=True)


@router.get("/home")
async def index(request: Request):
    user = None
    token = request.cookies.get("auth_token")
    if token:
        import httpx
        headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                str(request.base_url) + "users/me",
                headers=headers
            )
            if resp.status_code == 200:
                user = resp.json()
    return templates.TemplateResponse(
        "index.html", {"request": request, "user": user}
    )
