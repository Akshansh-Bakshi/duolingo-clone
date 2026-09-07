from __future__ import annotations

import datetime as dt

from sqlalchemy import Date, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class DailyActivity(Base):
    """
    Tracks XP earned by a user on a given calendar date. This is the
    source of truth for both the streak calculation and the "X / Y XP
    today" daily goal indicator. One row per (user, date) — enforced by a
    unique constraint — with `xp_earned` accumulated across the day.
    """

    __tablename__ = "daily_activity"
    __table_args__ = (UniqueConstraint("user_id", "activity_date", name="uq_user_date"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    activity_date: Mapped[dt.date] = mapped_column(Date, nullable=False)
    xp_earned: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    user: Mapped["User"] = relationship("User", back_populates="daily_activities")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<DailyActivity user_id={self.user_id} date={self.activity_date} xp={self.xp_earned}>"
