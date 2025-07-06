from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates
import httpx
from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

router = APIRouter()


@router.get("/tasks", response_class=HTMLResponse)
async def tasks_page(
    request: Request,
):
    base_url = str(request.base_url)
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{base_url}tasks/")
        tasks = resp.json() if resp.status_code == 200 else []
    return templates.TemplateResponse(
        "tasks.html",
        {"request": request, "tasks": tasks},
    )
