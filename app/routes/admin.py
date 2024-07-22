from fastapi import APIRouter, Depends

from app.schemas.books import Book

from app.services.books import create_book

router = APIRouter()


@router.post(
    "/create-book",
    summary="Создать новую книгу",
    description="Создает новую книгу в базе данных и загружает обложку.",
    response_description="Информация о созданной книге и путь к обложке",
    response_model=dict[str, Book],
)
async def upload_file(book: Book = Depends(create_book)):
    """
    Создает новую книгу и загружает обложку.

    Этот эндпоинт принимает информацию о книге и файл обложки,
    создает новую запись в базе данных и сохраняет обложку.

    HTTPMethods:
    - POST

    Parameters:
    - file (UploadFile): Файл обложки книги
    - title (str): Название книги
    - author (str): Автор книги
    - side (str): Сторона обложки (например, "front" или "back")

    Returns:
    - dict: Словарь, содержащий путь к сохраненному изображению обложки и информацию о книге
    """
    return {"book": book}
