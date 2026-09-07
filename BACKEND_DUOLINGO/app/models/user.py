from __future__ import annotations

import datetime as dt

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class User(Base):
    """
    A learner. Real authentication is out of scope for this project — the
    backend operates against a single seeded default learner (and any
    additional seeded learners used only to populate the leaderboard).
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)

    xp: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    streak: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    hearts: Mapped[int] = mapped_column(Integer, nullable=False, default=5)
    gems: Mapped[int] = mapped_column(Integer, nullable=False, default=500)
    daily_goal: Mapped[int] = mapped_column(Integer, nullable=False, default=50)

    last_activity: Mapped[dt.datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[dt.datetime] = mapped_column(DateTime, default=dt.datetime.utcnow, nullable=False)

    # --- Relationships -------------------------------------------------
    skill_progress: Mapped[list["UserSkillProgress"]] = relationship(
        "UserSkillProgress", back_populates="user", cascade="all, delete-orphan"
    )
    lesson_attempts: Mapped[list["LessonAttempt"]] = relationship(
        "LessonAttempt", back_populates="user", cascade="all, delete-orphan"
    )
    daily_activities: Mapped[list["DailyActivity"]] = relationship(
        "DailyActivity", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:  # pragma: no cover - debugging helper
        return f"<User id={self.id} username={self.username!r} xp={self.xp}>"
