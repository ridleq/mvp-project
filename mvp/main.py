from fastapi import FastAPI
from sqladmin import Admin

from mvp.core.admin import UserAdmin, TaskAdmin, TeamAdmin
from mvp.core.config import settings
from mvp.api.routers import main_router
from mvp.core.db import engine

app = FastAPI(title=settings.app_title)

admin = Admin(app, engine)
admin.add_view(UserAdmin)
admin.add_view(TaskAdmin)
admin.add_view(TeamAdmin)


app.include_router(main_router)
