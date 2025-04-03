from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "postgresql+psycopg2://admin:admin@localhost:5432/admin"

engine = create_engine(
    DATABASE_URL,
    paramstyle="format",
    connect_args={"client_encoding": "utf8", "options": "-c client_encoding=utf8"},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
