from pydantic import BaseModel, EmailStr, constr


class EmailSchema(BaseModel):
    email: EmailStr


class VerifyCode(BaseModel):
    email: EmailStr
    code: constr(min_length=6, max_length=6, strict=True)
