from fastapi import Request
from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.models.profile import Profile
from app.services.auth import get_username_from_token


def get_user_by_username(db: Session, username: str):
    return db.query(Profile).filter(Profile.username == username).first()


def create_user(db: Session, username: str):
    db_user = Profile(username=username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def get_or_create_user_db(request: Request):
    with SessionLocal() as db:
        username = get_username_from_token(request)
        user = get_user_by_username(db, username)
        if user is None:
            user = create_user(db, username)
        return user
