from typing import Dict

from fastapi import APIRouter, BackgroundTasks, Response

from app.schemas.auth import EmailSchema, VerifyCode, VerifyToken, MessageResponse
from app.services.auth import send_verification_code_email, create_access_token

router = APIRouter()


@router.post(
    "/request-verification-code",
    summary="Отправка кода подтверждения на почту",
    description="Генерирует код подтверждения и отправляет его на указанный email адрес.",
    response_description="Ответ что все создано",
    response_model=MessageResponse,
)
async def request_verification_code(
    background_tasks: BackgroundTasks, email: EmailSchema
):
    """
    Отправляет код подтверждения на указанный email адрес.

    HTTPMethods:
    - POST

    Parameters:
    - email (EmailSchema): Объект, содержащий email адрес пользователя

    Returns:
    - dict: Сообщение о успешной отправке кода
    """
    await send_verification_code_email(background_tasks, email)
    return {"message": "Код подтверждения отправлен на вашу электронную почту"}


@router.post(
    "/verify-code",
    summary="Проверка кода подтверждения",
    description="Проверяет код подтверждения и, в случае успеха, создает и устанавливает токен доступа.",
    response_description="Токен доступа",
)
async def verify_code_route(verify: VerifyCode, response: Response):
    """
    Проверяет код подтверждения и создает токен доступа.

    HTTPMethods:
    - POST

    Parameters:
    - verify (VerifyCode): Объект, содержащий email и код подтверждения
    - response (Response): Объект ответа FastAPI для установки куки

    Returns:
    - dict: Результат проверки кода. В случае успеха содержит токен доступа.
    """
    result = await create_access_token(verify)
    if result.get("access_token"):
        response.set_cookie(
            key="access_token",
            value=result["access_token"],
            httponly=True,
            max_age=1800,
            expires=1800,
            secure=False,
            path="/",
        )

    return result
