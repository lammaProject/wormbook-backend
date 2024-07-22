from fastapi.security import HTTPBearer
from pydantic import BaseModel, EmailStr, constr


bearer_scheme = HTTPBearer()


class EmailSchema(BaseModel):
    email: EmailStr


class VerifyCode(BaseModel):
    email: EmailStr
    code: constr(min_length=6, max_length=6, strict=True)


class VerifyToken(BaseModel):
    access_token: str


class MessageResponse(BaseModel):
    message: str
