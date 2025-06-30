from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Enum
from sqlalchemy.orm import relationship

from mvp.core.db import Base
from mvp.utils.user_role import UserRole
from mvp.models.team import team_user_association


class User(SQLAlchemyBaseUserTable[int], Base):
    role = Column(Enum(UserRole), default=UserRole.USER)
    tasks = relationship("Task", back_populates="executor")
    comments = relationship("Comment", back_populates="author")
    administered_teams = relationship("Team", back_populates="admin")
    teams = relationship(
        "Team",
        secondary=team_user_association,
        back_populates="members"
    )
