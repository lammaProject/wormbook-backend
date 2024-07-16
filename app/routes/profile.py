from fastapi import APIRouter, Depends

from app.services.profile import get_or_create_user
from app.models.profile import Profile

router = APIRouter()


@router.get(
    "/",
    summary="Получение пользователя",
)
async def get_profile(user: Profile = Depends(get_or_create_user)):
    return {"id": user.id, "username": user.username, "role": user.role}
