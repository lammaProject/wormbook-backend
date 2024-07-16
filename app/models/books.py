import enum
from sqlalchemy import Column, Integer, String, Date, Enum
from app.config.database import Base


class CategoryEnum(enum.Enum):
    adventure = "adventure"
    romance = "romance"
    criminal = "criminal"
    comedy = "comedy"


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    cover_image = Column(String)
