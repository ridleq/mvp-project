from fastapi_users import schemas
from pydantic import ConfigDict, Optional

from models.user import UserRole


class UserRead(schemas.BaseUser[int]):
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


class UserCreate(schemas.BaseUserCreate):
    role: Optional[UserRole] = UserRole.USER

    def validate_role(cls, valid_role):
        if valid_role not in list(UserRole):
            raise ValueError("Invalid user role")
        return valid_role


class UserUpdate(schemas.BaseUserUpdate):
    role: Optional[UserRole] = None
