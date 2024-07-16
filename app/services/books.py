import os
import shutil

from fastapi import UploadFile, File, Form

from app.config.settings import UPLOAD_CONFIG
from app.database.books import create_book_db, get_book_db
from app.schemas.books import BookCreate, BookGet


async def get_book(book: BookGet):
    return await get_book_db(book)


async def create_book(
    file: UploadFile = File(...),
    title: str = Form(...),
    author: str = Form(...),
    side: str = Form(...),
):
    file_extension = os.path.splitext(file.filename)[1]
    new_filename = f"{author}_{title}_{side}{file_extension}"
    file_location = os.path.join(UPLOAD_CONFIG["BOOKS_COVER"], new_filename)
    os.makedirs(os.path.dirname(file_location), exist_ok=True)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return await create_book_db(
        BookCreate(title=title, author=author, cover_image=file_location)
    )
