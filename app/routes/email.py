import random
import string
from datetime import datetime, timedelta

import jwt
from fastapi import APIRouter, BackgroundTasks, Response
from fastapi_mail import MessageSchema, FastMail, ConnectionConfig
from pydantic import EmailStr

from app.config.settings import MAIL_CONFIG
from app.config.settings import TOKEN_CONFIG

router = APIRouter()

verification_codes = {}


def generate_verification_code():
    characters = string.digits
    code = "".join(random.choice(characters) for _ in range(6))
    return code


def create_access_token(email: str, expires_delta: timedelta = None):
    to_encode = {"sub": email}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, TOKEN_CONFIG.SECRET_KEY, algorithm=TOKEN_CONFIG.ALGORITHM
    )
    return encoded_jwt


async def send_verification_code_email(
    background_tasks: BackgroundTasks, email: EmailStr, code: str
):
    message = MessageSchema(
        subject="Код подтверждения",
        recipients=[email],
        body=f"Ваш код подтверждения: {code}",
        subtype="plain",
    )

    verification_codes[email] = code
    fm = FastMail(ConnectionConfig(**MAIL_CONFIG))
    background_tasks.add_task(fm.send_message, message)


@router.post("/request-verification-code")
async def request_verification_code(background_tasks: BackgroundTasks, email: EmailStr):
    code = generate_verification_code()
    await send_verification_code_email(background_tasks, email, code)

    return {"message": "Код подтверждения отправлен на вашу электронную почту"}


@router.post("/verify-code")
async def verify_code(email: EmailStr, code: str, response: Response):
    stored_code = verification_codes.get(email)

    if stored_code is None or code != stored_code:
        return {"message": "Неверный код подтверждения"}

    verification_codes.pop(email)

    access_token = create_access_token(email=email.lower())

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=1800,  # Время жизни cookie (в данном случае 30 минут)
        expires=1800,
    )

    return {"message": "Код подтверждения успешно проверен"}
