from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

import enum
from sqlalchemy import Column, Enum
from mvp.core.db import Base


class UserRole(str, enum.Enum):
    USER = "user"
    MANAGER = "manager"
    TEAM_ADMIN = "team_admin"


class User(SQLAlchemyBaseUserTable[int], Base):
    role = Column(Enum(UserRole), default=UserRole.USER)
