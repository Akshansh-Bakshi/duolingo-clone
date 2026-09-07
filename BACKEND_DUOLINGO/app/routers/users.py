from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.user import UserMeResponse
from app.services import user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserMeResponse)
def get_me(db: Session = Depends(get_db)) -> UserMeResponse:
    """Returns the default learner's current stats, including today's XP."""
    user = user_service.get_default_user(db)
    daily_xp = user_service.get_daily_xp(db, user.id)
    return UserMeResponse(
        id=user.id,
        username=user.username,
        xp=user.xp,
        streak=user.streak,
        hearts=user.hearts,
        gems=user.gems,
        daily_goal=user.daily_goal,
        daily_xp=daily_xp,
    )
