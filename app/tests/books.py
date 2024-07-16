import pytest
from app.main import app
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_book():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/books/1")  # Предположим, что у нас есть книга с ID 1
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Название книги",
        "author": "Автор книги",
        "published_year": 2021,
    }
