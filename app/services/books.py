import os
import shutil

from fastapi import UploadFile, File, Form

from app.config.settings import UPLOAD_CONFIG
from app.database.books import create_book_db, get_book_db, get_books_db
from app.schemas.books import BookCreate, BookGet


async def get_book(book: BookGet):
    """
    Получает информацию о конкретной книге.

    Args:
        book (BookGet): Объект с данными для поиска книги.

    Returns:
        dict: Информация о запрошенной книге.
    """
    return await get_book_db(book)


async def get_books():
    """
    Получает список всех книг.

    Returns:
        list: Список всех книг в базе данных.
    """
    return await get_books_db()


async def create_book(
    file: UploadFile = File(...),
    title: str = Form(...),
    author: str = Form(...),
    side: str = Form(...),
):
    """
    Создает новую книгу и сохраняет ее обложку.

    Args:
        file (UploadFile): Файл обложки книги.
        title (str): Название книги.
        author (str): Автор книги.
        side (str): Сторона обложки (например, "front" или "back").

    Returns:
        dict: Информация о созданной книге.

    Raises:
        HTTPException: В случае ошибки при сохранении файла или создании записи в БД.
    """
    file_extension = os.path.splitext(file.filename)[1]
    new_filename = f"{author}_{title}_{side}{file_extension}"
    file_location = os.path.join(UPLOAD_CONFIG["BOOKS_COVER"], new_filename)
    os.makedirs(os.path.dirname(file_location), exist_ok=True)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return await create_book_db(
        BookCreate(title=title, author=author, cover_image=file_location)
    )
