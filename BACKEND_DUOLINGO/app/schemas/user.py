from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class UserMeResponse(BaseModel):
    """Response for GET /api/users/me — spec section 10."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    xp: int
    streak: int
    hearts: int
    gems: int
    daily_goal: int
    daily_xp: int  # computed: XP earned today, not a raw column
