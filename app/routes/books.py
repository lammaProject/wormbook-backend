from fastapi import APIRouter, Depends
from app.services.books import get_book, get_books
from app.schemas.books import Book

router = APIRouter()


@router.get(
    "/",
    summary="Получить список всех книг",
    description="Возвращает список всех доступных книг в библиотеке.",
    response_description="Возвращает список всех доступных книг в библиотеке.",
    response_model=dict[str, list[Book]],
)
async def get_books(books: list[Book] = Depends(get_books)):
    """
    Получает список всех книг.

    HTTPMethods:
    - GET

    Parameters:
    - books (List[Book]): Список объектов книг, полученный через зависимость get_books

    Returns:
    - dict: Словарь, содержащий список всех книг
    """
    return {"books": books}


@router.get(
    "/book",
    summary="Получить информацию о книге",
    description="Возвращает детальную информацию о конкретной книге.",
    response_description="Возвращает детальную информацию о конкретной книге.",
    response_model=Book,
)
async def get_book(book: Book = Depends(get_book)):
    """
    Получает информацию о конкретной книге.

    HTTPMethods:
    - GET

    Parameters:
    - book (Book): Объект книги, полученный через зависимость get_book

    Returns:
    - dict: Словарь, содержащий информацию о книге
    """
    return {"book": book}
