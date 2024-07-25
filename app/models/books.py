from sqlalchemy import Column, Integer, String, Date, Enum
from app.config.database import Base
from app.schemas.books import CategoryEnum


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    category = Column(Enum(CategoryEnum))
    rating = Column(Integer)
    front_file = Column(String)
    back_file = Column(String)
    bot_file = Column(String)
