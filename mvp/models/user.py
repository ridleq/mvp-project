from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Enum
from sqlalchemy.orm import relationship

from mvp.core.db import Base
from mvp.utils.user_role import UserRole


class User(SQLAlchemyBaseUserTable[int], Base):
    role = Column(Enum(UserRole), default=UserRole.USER)
    tasks = relationship("Task", back_populates="executor")
    comments = relationship("Comment", back_populates="author")
