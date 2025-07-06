from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_303_SEE_OTHER
from pathlib import Path

import os

router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


@router.get("/auth/login")
async def login_get(request: Request):
    return templates.TemplateResponse(
        "login.html", {"request": request, "error": None}
    )


@router.post("/auth/login")
async def login_post(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
):
    # ручной запрос к авторизации API
    import httpx
    async with httpx.AsyncClient() as client:
        response = await client.post(
            str(request.base_url) + "auth/jwt/login",  # путь к API
            data={"username": email, "password": password},
            headers={"accept": "application/json"},
        )
    if response.status_code == 200:
        token = response.json()["access_token"]
        response = RedirectResponse("/home", status_code=HTTP_303_SEE_OTHER)
        response.set_cookie("auth_token", token, httponly=True, max_age=3600)
        return response
    else:
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": "Неверная почта или пароль",
            },
            status_code=400
        )


@router.get("/auth/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/home", status_code=303)
    response.delete_cookie("auth_token")
    return response
