from sqladmin import ModelView
from mvp.models.user import User
from mvp.models.task import Task
from mvp.models.team import Team


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email]
    column_searchable_list = [User.id]
    column_sortable_list = [User.id]
    page_size = 10


class TaskAdmin(ModelView, model=Task):
    column_list = [
        Task.id,
        Task.description,
        Task.deadline,
        Task.status,
        Task.executor_id,
    ]
    column_sortable_list = [Task.id]
    page_size = 10


class TeamAdmin(ModelView, model=Team):
    column_list = [
        Team.name,
        Team.admin_id,
        Team.members,
    ]
    column_sortable_list = [Team.id]
    page_size = 10
