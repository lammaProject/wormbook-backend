import random
import string
from datetime import datetime, timedelta
from typing import Dict

import jwt
from fastapi import BackgroundTasks, Request
from fastapi_mail import MessageSchema, FastMail, ConnectionConfig

from app.config.settings import TOKEN_CONFIG, MAIL_CONFIG
from app.schemas.auth import EmailSchema, VerifyCode

verification_codes: Dict[str, str] = {}


async def create_access_token(verify: VerifyCode, expires_delta: timedelta = None):
    """
    Создает JWT токен доступа после проверки кода подтверждения.

    Args:
        verify (VerifyCode): Объект с email и кодом подтверждения.
        expires_delta (timedelta, optional): Время жизни токена. По умолчанию None.

    Returns:
        dict: Объект с токеном доступа или сообщением об ошибке.
    """
    stored_code = verification_codes.get(verify.email)

    if stored_code is None or verify.code != stored_code:
        return {"message": "Неверный код"}

    verification_codes.pop(verify.email)

    to_encode = {"sub": verify.email}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=4, minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, TOKEN_CONFIG["SECRET_KEY"], algorithm=TOKEN_CONFIG["ALGORITHM"]
    )
    return {"access_token": encoded_jwt}


async def send_verification_code_email(
    background_tasks: BackgroundTasks, email: EmailSchema
):
    """
    Отправляет код подтверждения на указанный email.

    Args:
        background_tasks (BackgroundTasks): Объект для выполнения задач в фоновом режиме.
        email (EmailSchema): Объект с email адресом получателя.
    """
    characters = string.digits
    code = "".join(random.choice(characters) for _ in range(6))
    verification_codes[email.email] = code
    message = MessageSchema(
        subject="Код подтверждения",
        recipients=[email.email],
        body=f"Ваш код подтверждения: {code}",
        subtype="plain",
    )

    fm = FastMail(ConnectionConfig(**MAIL_CONFIG))
    background_tasks.add_task(fm.send_message, message)


def get_username_from_token(request: Request):
    """
    Извлекает имя пользователя (email) из JWT токена в куки запроса.

    Args:
        request (Request): Объект запроса FastAPI.

    Returns:
        str: Имя пользователя (email) из токена.
    """
    token = request.cookies.get("access_token")
    payload = jwt.decode(
        token, TOKEN_CONFIG["SECRET_KEY"], algorithms=[TOKEN_CONFIG["ALGORITHM"]]
    )
    return payload.get("sub")
