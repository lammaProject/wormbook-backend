import enum
from pydantic import BaseModel
from fastapi import UploadFile, File


class CategoryEnum(enum.Enum):
    adventure = "adventure"
    romance = "romance"
    criminal = "criminal"
    comedy = "comedy"


class BookCreate(BaseModel):
    title: str
    author: str
    front_file: str
    back_file: str
    bot_file: str
    category: CategoryEnum
    rating: int


class Book(BaseModel):
    id: int
    title: str
    author: str
    front_file: UploadFile = File(...)
    back_file: UploadFile = File(...)
    bot_file: UploadFile = File(...)
    rating: float
    category: CategoryEnum


class BookGet(BaseModel):
    id: str
