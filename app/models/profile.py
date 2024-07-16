import enum
from sqlalchemy import Column, Integer, String, Enum
from app.config.database import Base


class UserRole(enum.Enum):
    admin = "admin"
    user = "user"
    mod = "mod"


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    role = Column(Enum(UserRole))
