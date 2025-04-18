from typing import Optional

from app.config.database import SessionLocal
from app.schemas.books import BookCreate, BookGet
from app.models.books import Book


async def get_book_db(book_id: Optional[int] = None):
    with SessionLocal() as db:
        return db.query(Book).filter(Book.id == book_id).first()


async def get_books_db():
    with SessionLocal() as db:
        return db.query(Book).all()


async def create_book_db(book: BookCreate):
    with SessionLocal() as db:
        db_book = Book(**book.dict())
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        return db_book
