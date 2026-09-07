"""
User-related business logic: fetching the default learner and computing
the "XP earned today" figure used throughout the API.
"""
from __future__ import annotations

import datetime as dt

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import DailyActivity, User


def get_default_user(db: Session) -> User:
    """
    Return the single seeded default learner the whole backend operates
    as (real auth is out of scope per the spec). Raises if the seed step
    hasn't been run — callers should treat that as a 500, since it
    indicates a misconfigured deployment rather than a client error.
    """
    user = db.query(User).filter(User.username == settings.DEFAULT_USERNAME).first()
    if user is None:
        raise RuntimeError(
            f"Default user '{settings.DEFAULT_USERNAME}' not found. "
            "Run the seed script (python -m app.seed.seed_data) first."
        )
    return user


def get_daily_xp(db: Session, user_id: int, on_date: dt.date | None = None) -> int:
    """XP the user has earned so far on `on_date` (defaults to today, UTC)."""
    target_date = on_date or dt.datetime.utcnow().date()
    activity = (
        db.query(DailyActivity)
        .filter(DailyActivity.user_id == user_id, DailyActivity.activity_date == target_date)
        .first()
    )
    return activity.xp_earned if activity else 0
