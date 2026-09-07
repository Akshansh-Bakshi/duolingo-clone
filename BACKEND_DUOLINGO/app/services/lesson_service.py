"""
Business logic for the lesson player's core loop: fetching a lesson and
validating a submitted answer against the authoritative correct_answer
stored in the database (spec section 10 "Lessons").
"""
from __future__ import annotations

from sqlalchemy.orm import Session, joinedload

from app.core.config import settings
from app.models import Exercise, Lesson, User


def get_lesson(db: Session, lesson_id: int) -> Lesson | None:
    return (
        db.query(Lesson)
        .options(joinedload(Lesson.exercises))
        .filter(Lesson.id == lesson_id)
        .first()
    )


def _normalize(text: str) -> str:
    """Loose, forgiving comparison: trims whitespace and ignores case."""
    return " ".join(text.strip().lower().split())


def check_answer(exercise: Exercise, submitted_answer: str) -> bool:
    """
    Compare a submitted answer to the exercise's correct_answer.

    All current exercise types (multiple_choice, translate, word_bank,
    match, fill_blank, type_answer) store their correct answer as a single
    canonical string, so a normalized string comparison is sufficient and
    keeps this function type-agnostic. `data`/`options` are used by the
    frontend for rendering only, never for validation.
    """
    return _normalize(submitted_answer) == _normalize(exercise.correct_answer)


class OutOfHeartsError(Exception):
    """Raised when a user with 0 hearts tries to submit another answer."""


def submit_answer(
    db: Session, user: User, lesson: Lesson, exercise: Exercise, answer: str
) -> tuple[bool, int, bool]:
    """
    Validate an answer and, if wrong, deduct a heart.

    Returns (is_correct, hearts_remaining, just_ran_out_of_hearts).
    Raises OutOfHeartsError if the user already had 0 hearts before
    submitting (the frontend should have blocked this, but the backend
    stays authoritative).
    """
    if user.hearts <= 0:
        raise OutOfHeartsError("User has no hearts remaining.")

    is_correct = check_answer(exercise, answer)
    just_ran_out = False

    if not is_correct:
        user.hearts = max(0, user.hearts - 1)
        just_ran_out = user.hearts == 0
        db.add(user)
        db.commit()
        db.refresh(user)

    return is_correct, user.hearts, just_ran_out
