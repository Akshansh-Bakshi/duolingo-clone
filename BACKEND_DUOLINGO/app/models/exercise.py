from __future__ import annotations

import enum

from sqlalchemy import Enum, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ExerciseType(str, enum.Enum):
    """Supported exercise types (spec section 5 / 9)."""

    MULTIPLE_CHOICE = "multiple_choice"
    TRANSLATE = "translate"
    WORD_BANK = "word_bank"
    MATCH = "match"
    FILL_BLANK = "fill_blank"
    TYPE_ANSWER = "type_answer"


class Exercise(Base):
    """
    A single exercise within a Lesson.

    `options` holds choice-style data (multiple choice options, word bank
    tokens) as JSON. `data` holds any other exercise-specific structured
    payload (e.g. match pairs). Both are optional/nullable since not every
    exercise type needs them. SQLAlchemy's JSON type stores as TEXT under
    SQLite, matching the spec's "JSON/TEXT" column description.
    """

    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"), nullable=False, index=True)
    type: Mapped[ExerciseType] = mapped_column(Enum(ExerciseType), nullable=False)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    correct_answer: Mapped[str] = mapped_column(Text, nullable=False)
    options: Mapped[list | dict | None] = mapped_column(JSON, nullable=True)
    data: Mapped[list | dict | None] = mapped_column(JSON, nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    lesson: Mapped["Lesson"] = relationship("Lesson", back_populates="exercises")

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Exercise id={self.id} type={self.type}>"
