from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict

from app.models.exercise import ExerciseType


class ExercisePublic(BaseModel):
    """
    Exercise as sent to the frontend for rendering.

    Deliberately omits `correct_answer` — the backend is authoritative for
    answer checking (spec section 10), so the correct answer must never be
    shipped to the client ahead of submission.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    lesson_id: int
    type: ExerciseType
    question: str
    options: Any | None = None
    data: Any | None = None
    order_index: int


class ExerciseSubmitRequest(BaseModel):
    """Request body for POST /api/lessons/{lesson_id}/submit."""

    exercise_id: int
    answer: str


class ExerciseSubmitResponse(BaseModel):
    """Response for POST /api/lessons/{lesson_id}/submit."""

    correct: bool
    correct_answer: str
    hearts_remaining: int
    out_of_hearts: bool
    message: str
