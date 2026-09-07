from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Lesson(Base):
    """A single lesson within a Skill, made up of an ordered list of Exercises."""

    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    skill: Mapped["Skill"] = relationship("Skill", back_populates="lessons")
    exercises: Mapped[list["Exercise"]] = relationship(
        "Exercise",
        back_populates="lesson",
        cascade="all, delete-orphan",
        order_by="Exercise.order_index",
    )
    attempts: Mapped[list["LessonAttempt"]] = relationship(
        "LessonAttempt", back_populates="lesson", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Lesson id={self.id} title={self.title!r}>"
