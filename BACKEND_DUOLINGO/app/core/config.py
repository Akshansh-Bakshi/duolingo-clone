"""
Application configuration.

Centralizes all environment-driven and constant settings so the rest of
the codebase never hardcodes values like the database path, CORS origins,
or gamification constants. Keeping these in one place is what lets a
developer change deployment settings without touching business logic.
"""
from __future__ import annotations

import os
from pathlib import Path


class Settings:
    """
    Simple settings object populated from environment variables with
    sensible local-dev defaults. We intentionally avoid pydantic-settings
    here to keep the dependency footprint small (per the spec's guidance
    to avoid unnecessary dependencies) — plain os.environ reads are enough
    for this project's scope.
    """

    # --- General -----------------------------------------------------
    APP_NAME: str = "Duolingo Clone API"
    API_PREFIX: str = "/api"
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"

    # --- Paths ---------------------------------------------------------
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent  # BACKEND_DUOLINGO/
    DB_FILE: Path = BASE_DIR / os.getenv("DB_FILE_NAME", "duolingo.db")

    # --- Database --------------------------------------------------------
    SQLALCHEMY_DATABASE_URL: str = os.getenv(
        "DATABASE_URL", f"sqlite:///{DB_FILE}"
    )

    # --- CORS ------------------------------------------------------------
    # Comma-separated list of allowed origins, e.g. "http://localhost:3000,https://myapp.com"
    CORS_ORIGINS: list[str] = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:3000,http://127.0.0.1:3000",
        ).split(",")
        if origin.strip()
    ]

    # --- Default learner ---------------------------------------------
    # Real authentication is out of scope for this assignment; the backend
    # always operates on behalf of this single seeded learner.
    DEFAULT_USERNAME: str = os.getenv("DEFAULT_USERNAME", "Learner")

    # --- Gamification constants ---------------------------------------
    INITIAL_HEARTS: int = 5
    MAX_HEARTS: int = 5
    INITIAL_GEMS: int = 500
    DEFAULT_DAILY_GOAL_XP: int = 50

    XP_LESSON_COMPLETE: int = 20
    XP_PERFECT_LESSON: int = 30  # awarded instead of XP_LESSON_COMPLETE when no mistakes

    # Mocked practice/refill: how many hearts a practice session restores.
    PRACTICE_HEARTS_RESTORED: int = 5


settings = Settings()
