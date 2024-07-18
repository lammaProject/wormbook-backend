from fastapi import APIRouter, BackgroundTasks, Response

from app.schemas.auth import EmailSchema, VerifyCode
from app.services.auth import send_verification_code_email, create_access_token

router = APIRouter()


@router.post(
    "/request-verification-code",
    summary="Отправка кода на почту",
    description="Какой то",
)
async def request_verification_code(
    background_tasks: BackgroundTasks, email: EmailSchema
):
    await send_verification_code_email(background_tasks, email)
    return {"message": "Код подтверждения отправлен на вашу электронную почту"}


@router.post("/verify-code")
async def verify_code_route(verify: VerifyCode, response: Response):
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
