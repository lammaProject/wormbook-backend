from fastapi import APIRouter, Depends

from app.services.profile import get_or_create_user
from app.schemas.profile import UserProfile

router = APIRouter()


@router.get(
    "/",
    summary="Получение профиля пользователя",
    description="Возвращает информацию о профиле текущего пользователя или создает новый профиль, если пользователь не существует.",
    response_description="Информация о профиле пользователя",
    response_model=UserProfile,
)
async def get_profile(user: UserProfile = Depends(get_or_create_user)):
    """
    Получает профиль текущего пользователя или создает новый, если пользователь не существует.

    Эта функция использует зависимость get_or_create_user для получения или создания пользователя
    на основе данных аутентификации.

    HTTPMethods:
    - GET

    Parameters:
    - user (Profile): Объект профиля пользователя, полученный через зависимость get_or_create_user

    Returns:
    - dict: Словарь, содержащий id, имя пользователя и роль
    """
    return {"id": user.id, "username": user.username, "role": user.role.value}
