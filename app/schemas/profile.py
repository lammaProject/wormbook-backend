from enum import Enum

from pydantic import BaseModel


class UserRole(str, Enum):
    admin = "admin"
    user = "user"
    mod = "mod"


class UserProfile(BaseModel):
    id: int
    username: str
    role: UserRole
