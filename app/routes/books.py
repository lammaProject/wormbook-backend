from fastapi import APIRouter, Depends
from app.services.books import get_book
from app.schemas.books import Book

router = APIRouter()


@router.get("/get-book")
async def get_book(book: Book = Depends(get_book)):
    return {"book": book}
