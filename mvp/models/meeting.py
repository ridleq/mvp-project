from sqlalchemy import (
    Column, DateTime, ForeignKey, Table
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from mvp.core.db import Base

meeting_user_association = Table(
    'meeting_user_association',
    Base.metadata,
    Column('meeting_id', ForeignKey('meeting.id'), primary_key=True),
    Column('user_id', ForeignKey('user.id'), primary_key=True)
)


class Meeting(Base):
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)

    participants = relationship(
        "User",
        secondary=meeting_user_association,
        back_populates="meetings",
        lazy="selectin"
    )

    @hybrid_property
    def participant_ids(self):
        return [user.id for user in self.participants]
