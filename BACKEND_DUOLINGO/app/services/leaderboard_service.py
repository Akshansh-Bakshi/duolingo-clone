"""Business logic for the leaderboard (spec section 10 "Leaderboard")."""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.models import User


def get_leaderboard(db: Session, limit: int = 20) -> list[dict]:
    users = db.query(User).order_by(User.xp.desc()).limit(limit).all()
    return [
        {"rank": index + 1, "username": u.username, "xp": u.xp}
        for index, u in enumerate(users)
    ]
