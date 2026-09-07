from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.profile import LeaderboardEntry, LeaderboardResponse
from app.services import leaderboard_service

router = APIRouter(prefix="/leaderboard", tags=["leaderboard"])


@router.get("", response_model=LeaderboardResponse)
def get_leaderboard(db: Session = Depends(get_db)) -> LeaderboardResponse:
    """Returns seeded users ordered by XP, descending."""
    entries = leaderboard_service.get_leaderboard(db)
    return LeaderboardResponse(entries=[LeaderboardEntry(**e) for e in entries])
