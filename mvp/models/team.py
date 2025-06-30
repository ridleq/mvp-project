from sqlalchemy import (
    Column, Integer, String, ForeignKey, Table, ForeignKeyConstraint
)
from sqlalchemy.orm import relationship
from mvp.core.db import Base

team_user_association = Table(
    "team_user_association",
    Base.metadata,
    Column("team_id", Integer),
    Column("user_id", Integer)
)


class Team(Base):
    name = Column(String(100), unique=True, nullable=False)
    admin_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    admin = relationship("User", back_populates="administered_teams")
    members = relationship(
        "User",
        secondary=team_user_association,
        back_populates="teams"
    )


team_user_association.append_constraint(
    ForeignKeyConstraint(["team_id"], ["team.id"])
)
team_user_association.append_constraint(
    ForeignKeyConstraint(["user_id"], ["user.id"])
)
