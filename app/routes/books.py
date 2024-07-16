from fastapi import APIRouter, Depends
from app.services.books import create_book, get_book
from app.schemas.books import Book

router = APIRouter()


@router.get("/get-book")
async def get_book(book: Book = Depends(get_book)):
    return {"book": book}


@router.post("/create-book")
async def upload_file(book: Book = Depends(create_book)):
    return {"path_to_img": book.cover_image, "book": book}
