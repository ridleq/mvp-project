from fastapi import FastAPI

from mvp.core.config import settings
from mvp.api.routers import main_router

app = FastAPI(title=settings.app_title)

app.include_router(main_router)
