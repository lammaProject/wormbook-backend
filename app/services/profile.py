from fastapi import Request
from app.database.profile import get_or_create_user_db


async def get_or_create_user(request: Request):
    return await get_or_create_user_db(request)
