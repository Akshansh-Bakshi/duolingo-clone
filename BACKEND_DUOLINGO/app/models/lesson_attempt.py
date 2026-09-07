from __future__ import annotations

import datetime as dt

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class LessonAttempt(Base):
    """
    A record of a learner attempting (and, if successful, completing) a
    lesson. Written once per attempt when the lesson finishes (either
    completed or failed via out-of-hearts) — this is the audit trail used
    to compute lesson history / stats, distinct from the live in-progress
    session state which lives entirely on the frontend.
    """

    __tablename__ = "lesson_attempts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"), nullable=False, index=True)

    score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)  # correct answers count
    xp_earned: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    hearts_lost: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    completed_at: Mapped[dt.datetime | None] = mapped_column(DateTime, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="lesson_attempts")
    lesson: Mapped["Lesson"] = relationship("Lesson", back_populates="attempts")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<LessonAttempt id={self.id} lesson_id={self.lesson_id} completed={self.completed}>"
