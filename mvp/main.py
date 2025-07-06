from fastapi import FastAPI
from sqladmin import Admin

from mvp.api.routers import main_router
from mvp.core.admin import TaskAdmin, TeamAdmin, UserAdmin
from mvp.core.config import settings
from mvp.core.db import engine
from mvp.web.index import router as index_router
from mvp.web.auth import router as auth_router
from mvp.web.tasks import router as task_router
from mvp.web.teams import router as teams_router
from mvp.web.meetings import router as meeting_router


app = FastAPI(title=settings.app_title)

admin = Admin(app, engine)
admin.add_view(UserAdmin)
admin.add_view(TaskAdmin)
admin.add_view(TeamAdmin)


app.include_router(main_router)
app.include_router(index_router)
app.include_router(auth_router)
app.include_router(task_router)
app.include_router(teams_router)
app.include_router(meeting_router)
