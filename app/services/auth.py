import random
import string
from datetime import datetime, timedelta
from typing import Dict

import jwt
from fastapi import Request
from fastapi_mail import MessageSchema, FastMail, ConnectionConfig
from starlette.responses import JSONResponse

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


async def send_verification_code_email(email: EmailSchema):
    try:
        characters = string.digits
        code = "".join(random.choice(characters) for _ in range(6))
        verification_codes[email.email] = code

        # Создаем более информативное сообщение
        body_content = f"""
        Здравствуйте!

        Ваш код подтверждения: {code}

        С уважением,
        Команда вашего сервиса
        """

        message = MessageSchema(
            subject="Код подтверждения для вашего аккаунта",
            recipients=[email.email],
            body=body_content,
            subtype="plain",
            headers={
                "X-Priority": "1",
                "Importance": "high",
                "X-MSMail-Priority": "High",
            },
        )

        fm = FastMail(ConnectionConfig(**MAIL_CONFIG))

        print(f"Attempting to send email to {email.email} with code {code}")
        print(f"SMTP settings: {MAIL_CONFIG['MAIL_SERVER']}:{MAIL_CONFIG['MAIL_PORT']}")

        await fm.send_message(message)

        print(f"Email sent successfully to {email.email}")
        return JSONResponse(status_code=200, content={"message": "email has been sent"})
    except Exception as e:
        print(f"Error sending email to {email.email}: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback

        print(traceback.format_exc())
        return JSONResponse(
            status_code=500, content={"message": f"Failed to send email: {str(e)}"}
        )


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
