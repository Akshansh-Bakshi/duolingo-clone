from __future__ import annotations

from pydantic import BaseModel


class SkillProgressItem(BaseModel):
    skill_id: int
    skill_title: str
    xp: int
    completion_percent: int
    crowns: int
    completed: bool


class ProgressResponse(BaseModel):
    """Response for GET /api/progress."""

    user_id: int
    xp: int
    streak: int
    hearts: int
    gems: int
    daily_goal: int
    daily_xp: int
    daily_goal_reached: bool
    skills: list[SkillProgressItem]


class PracticeResponse(BaseModel):
    """Response for POST /api/progress/practice (mocked hearts refill)."""

    hearts: int
    gems: int
    message: str
