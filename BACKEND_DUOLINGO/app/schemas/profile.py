from __future__ import annotations

from pydantic import BaseModel


class ProfileResponse(BaseModel):
    """Response for GET /api/profile."""

    username: str
    total_xp: int
    streak: int
    hearts: int
    gems: int
    completed_skills: int
    total_skills: int
    lessons_completed: int


class LeaderboardEntry(BaseModel):
    rank: int
    username: str
    xp: int


class LeaderboardResponse(BaseModel):
    """Response for GET /api/leaderboard."""

    entries: list[LeaderboardEntry]
