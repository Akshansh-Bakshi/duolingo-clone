from __future__ import annotations

import datetime as dt

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class UserSkillProgress(Base):
    """
    Tracks a single user's progress through a single skill.

    `completion_percent` and `crowns` are derived from how many of the
    skill's lessons have been completed (see services/progress_service.py).
    One row per (user, skill) pair — enforced by a unique constraint, since
    a learner has exactly one progress record per skill.
    """

    __tablename__ = "user_skill_progress"
    __table_args__ = (UniqueConstraint("user_id", "skill_id", name="uq_user_skill"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"), nullable=False, index=True)

    xp: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    completion_percent: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    crowns: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    completed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    updated_at: Mapped[dt.datetime] = mapped_column(
        DateTime, default=dt.datetime.utcnow, onupdate=dt.datetime.utcnow, nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="skill_progress")
    skill: Mapped["Skill"] = relationship("Skill", back_populates="progress_entries")

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"<UserSkillProgress user_id={self.user_id} skill_id={self.skill_id} "
            f"completion={self.completion_percent}%>"
        )
