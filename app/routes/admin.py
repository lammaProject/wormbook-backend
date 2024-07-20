from fastapi import APIRouter, Depends

from app.schemas.books import Book

from app.services.books import create_book

router = APIRouter()


@router.post("/create-book")
async def upload_file(book: Book = Depends(create_book)):
    return {"path_to_img": book.cover_image, "book": book}
