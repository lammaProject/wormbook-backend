import os
import shutil
from typing import Optional

from fastapi import UploadFile, File, Form, HTTPException

from app.config.settings import UPLOAD_CONFIG
from app.database.books import create_book_db, get_book_db, get_books_db
from app.schemas.books import BookCreate, CategoryEnum


def process_file(file_type, file, author):
    print(file_type, file, "file")
    file_location = os.path.join(UPLOAD_CONFIG["BOOKS_COVER"], author, file.filename)
    os.makedirs(os.path.dirname(file_location), exist_ok=True)

    try:
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return file_location
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Не удалось сохранить файл {file_type}: {str(e)}",
        )


async def get_book(book_id: Optional[int] = None):
    if book_id is None:
        return None
    return await get_book_db(book_id)


async def get_books():
    """
    Получает список всех книг.

    Returns:
        list: Список всех книг в базе данных.
    """
    return await get_books_db()


async def create_book(
    front_file: UploadFile = File(...),
    back_file: UploadFile = File(...),
    bot_file: UploadFile = File(...),
    title: str = Form(...),
    author: str = Form(...),
    category: CategoryEnum = Form(...),
    rating: Optional[int] = Form(None),
):
    """
    Создает новую книгу и сохраняет ее обложку.

    Returns:
        dict: Информация о созданной книге.

    Raises:
        HTTPException: В случае ошибки при сохранении файла или создании записи в БД.
        :param bot_file:
        :param back_file:
        :param front_file:
        :param rating:
        :param category:
        :param author:
        :param title;
    """
    print(front_file, back_file, bot_file, "FILESSS")

    file_locations = {
        "front_file": process_file("front_file", front_file, author=author),
        "back_file": process_file("back_file", back_file, author=author),
        "bot_file": process_file("bot_file", bot_file, author=author),
    }

    return await create_book_db(
        BookCreate(
            title=title,
            author=author,
            front_file=file_locations["front_file"],
            back_file=file_locations["back_file"],
            bot_file=file_locations["bot_file"],
            category=category,
            rating=rating or 0,
        )
    )
