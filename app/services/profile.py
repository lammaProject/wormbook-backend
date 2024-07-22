from fastapi import Request
from app.database.profile import get_or_create_user_db, get_user_by_username
from app.schemas.profile import UserProfile


async def get_or_create_user(request: Request):
    """
    Получает существующего пользователя или создает нового на основе данных запроса.

    Эта функция служит оберткой для вызова соответствующей функции базы данных.
    Она используется для получения или регистрации пользователя при каждом запросе.

    Args:
        request (Request): Объект запроса FastAPI, содержащий информацию о пользователе
                           (например, токен в заголовках или куки).

    Returns:
        User: {UserProfile} - Объект пользователя, созданный или полученный из базы данных.

    Raises:
        HTTPException: Может быть вызвано функцией базы данных в случае ошибки
                       аутентификации или создания пользователя.
    """
    return await get_or_create_user_db(request)
