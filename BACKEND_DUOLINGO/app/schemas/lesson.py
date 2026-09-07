from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from app.schemas.exercise import ExercisePublic


class LessonDetailResponse(BaseModel):
    """Response for GET /api/lessons/{lesson_id}."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    skill_id: int
    title: str
    order_index: int
    exercises: list[ExercisePublic]


class LessonCompleteRequest(BaseModel):
    """
    Request body for POST /api/lessons/{lesson_id}/complete.

    The frontend reports how the lesson session went; the backend remains
    authoritative by clamping/validating these values against the lesson's
    actual exercise count rather than trusting them blindly.
    """

    correct_count: int
    total_exercises: int
    hearts_lost: int = 0


class LessonCompleteResponse(BaseModel):
    """Response for POST /api/lessons/{lesson_id}/complete — a completion summary."""

    xp_earned: int
    total_xp: int
    perfect: bool
    skill_id: int
    skill_completion_percent: int
    skill_crowns: int
    skill_completed: bool
    streak: int
    daily_xp: int
    daily_goal: int
    daily_goal_reached: bool
    hearts_remaining: int
