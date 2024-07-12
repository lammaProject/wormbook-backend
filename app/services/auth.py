import random
import string
from datetime import datetime, timedelta
from typing import Dict

import jwt
from fastapi import BackgroundTasks
from fastapi_mail import MessageSchema, FastMail, ConnectionConfig

from app.config.settings import TOKEN_CONFIG, MAIL_CONFIG
from app.schemas.auth import EmailSchema, VerifyCode

verification_codes: Dict[str, str] = {}


def generate_verification_code():
    characters = string.digits
    code = "".join(random.choice(characters) for _ in range(6))
    return code


async def create_access_token(verify: VerifyCode, expires_delta: timedelta = None):
    stored_code = verification_codes.get(verify.email)

    if stored_code is None or verify.code != stored_code:
        return {"message": "Неверный код"}

    verification_codes.pop(verify.email)

    to_encode = {"sub": verify.email}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, TOKEN_CONFIG["SECRET_KEY"], algorithm=TOKEN_CONFIG["ALGORITHM"]
    )
    return {"access_token": encoded_jwt}


async def send_verification_code_email(
    background_tasks: BackgroundTasks, email: EmailSchema
):
    code = generate_verification_code()
    verification_codes[email.email] = code
    message = MessageSchema(
        subject="Код подтверждения",
        recipients=[email.email],
        body=f"Ваш код подтверждения: {code}",
        subtype="plain",
    )

    fm = FastMail(ConnectionConfig(**MAIL_CONFIG))
    background_tasks.add_task(fm.send_message, message)