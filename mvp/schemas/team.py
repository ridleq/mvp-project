from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class TeamBase(BaseModel):
    name: str
    user_ids: List[int] = Field(default_factory=list)


class TeamCreate(TeamBase):
    pass


class TeamUpdate(TeamBase):
    name: Optional[str] = None
    user_ids: Optional[List[int]] = None
    add: List[int] = Field(default_factory=list)
    remove: List[int] = Field(default_factory=list)


class Team(TeamBase):
    id: int
    admin_id: int

    model_config = ConfigDict(from_attributes=True)


class TeamMembersResponse(BaseModel):
    members: List[int]

    model_config = ConfigDict(from_attributes=True)
