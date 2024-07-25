from fastapi import FastAPI, Request, Depends, staticfiles
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import origins
from app.middleware import add_process_token
from app.routes import auth, profile, books, admin
from app.services.verify import verify_token, verify_admin
from app.config.database import Base, engine

app = FastAPI(
    title="WormBook",
    description="Это бэкенд для приложения",
    version="1.0.0",
)

app.mount(
    "/upload",
    staticfiles.StaticFiles(directory="upload"),
    name="upload",
)

Base.metadata.create_all(bind=engine, checkfirst=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def process_token_middleware(request: Request, call_next):
    return await add_process_token(request, call_next)


app.include_router(auth.router, tags=["Аутентификация"], prefix="/auth")
app.include_router(
    profile.router,
    tags=["Профиль"],
    prefix="/profile",
    dependencies=[Depends(verify_token)],
)
app.include_router(
    admin.router,
    tags=["Админка"],
    prefix="/admin",
    dependencies=[Depends(verify_token), Depends(verify_admin)],
)
app.include_router(books.router, tags=["Книги"], prefix="/books")
