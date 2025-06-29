from enum import Enum


class UserRole(str, Enum):
    USER = "user"
    MANAGER = "manager"
    TEAM_ADMIN = "team_admin"
