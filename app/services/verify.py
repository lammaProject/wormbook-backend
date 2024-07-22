import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from app.config.settings import TOKEN_CONFIG
from app.database.profile import get_or_create_user_db
from app.schemas.auth import bearer_scheme
from app.schemas.profile import UserProfile, UserRole


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    """
    Проверяет JWT токен и извлекает из него имя пользователя.

    Эта функция используется как зависимость для проверки аутентификации пользователя.

    Args:
        credentials (HTTPAuthorizationCredentials): Объект с учетными данными авторизации,
                                                    полученный из HTTP заголовка Authorization.

    Returns:
        str: Имя пользователя (обычно email), извлеченное из токена.

    Raises:
        HTTPException: Если токен недействителен или отсутствует,
                       вызывается исключение с кодом 401 Unauthorized.
    """
    token = credentials.credentials
    print(token)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не авторизованы",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        if token.startswith("Bearer "):
            token = token[len("Bearer ")]
        payload = jwt.decode(
            token,
            TOKEN_CONFIG["SECRET_KEY"],
            algorithms=[TOKEN_CONFIG["ALGORITHM"]],
        )
        username: str = payload.get("sub")
        print(payload)
        if username is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
    return username


async def verify_admin(user: UserProfile = Depends(get_or_create_user_db)):
    """
    Проверяет, имеет ли пользователь права администратора.

    Эта функция используется как зависимость для ограничения доступа к определенным эндпоинтам
    только для администраторов.

    Args:
        user (UserProfile): Профиль пользователя, полученный из базы данных.

    Returns:
        UserProfile: Профиль пользователя, если он имеет права администратора.

    Raises:
        HTTPException: Если пользователь не имеет прав администратора,
                       вызывается исключение с кодом 403 Forbidden.
    """
    if str(user.role) != str(UserRole.admin):
        raise HTTPException(
            status_code=403, detail="Access denied. Admin rights required."
        )
    return user
