from fastapi import FastAPI

from app.routes import email

app = FastAPI()

app.include_router(email.router)
