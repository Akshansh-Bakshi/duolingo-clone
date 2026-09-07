"""
SQLAlchemy engine, session factory, and declarative base.

This module owns everything related to *connecting* to the database.
Models import `Base` from here; routers/services get a session via the
`get_db` dependency. No business logic lives in this file.
"""
from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

# `check_same_thread` is required for SQLite when used with FastAPI, since
# FastAPI may access the same connection from different threads across a
# single request's lifecycle (e.g. with sync def endpoints run in a
# threadpool).
connect_args = (
    {"check_same_thread": False}
    if settings.SQLALCHEMY_DATABASE_URL.startswith("sqlite")
    else {}
)

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    FastAPI dependency that yields a database session for the duration of
    a single request and always closes it afterwards, even on error.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Create all tables that don't already exist.

    This is intentionally simple (no migrations framework) since the spec
    calls for SQLite with a hand-designed schema and no unnecessary
    infrastructure. Import all models before calling this so they are
    registered on `Base.metadata`.
    """
    # Imported here (not at module top) to avoid a circular import between
    # database.py and the model modules, which themselves import Base from
    # this file. Importing app.models registers every model class on
    # Base.metadata.
    import app.models  # noqa: F401

    Base.metadata.create_all(bind=engine)
