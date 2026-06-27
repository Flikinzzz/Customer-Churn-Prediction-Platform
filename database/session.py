"""Módulo de sesión y conexión a la base de datos."""

from collections.abc import Generator
from os import environ

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

DATABASE_URL = environ.get("DATABASE_URL", "sqlite:///./churn_prediction.db")

# Configuración especial si se usa SQLite para evitar bloqueos de hilos en FastAPI
engine_kwargs = {}
if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
