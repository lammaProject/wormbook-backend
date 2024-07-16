from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    author: str
    cover_image: str


class Book(BaseModel):
    id: int
    title: str
    author: str
    cover_image: str


class BookGet(BaseModel):
    title: str
    author: str
