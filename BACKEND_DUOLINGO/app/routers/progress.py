from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Skill, UserSkillProgress
from app.schemas.progress import PracticeResponse, ProgressResponse, SkillProgressItem
from app.services import progress_service, user_service

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("", response_model=ProgressResponse)
def get_progress(db: Session = Depends(get_db)) -> ProgressResponse:
    """Returns the default learner's overall + per-skill progress."""
    user = user_service.get_default_user(db)
    daily_xp = user_service.get_daily_xp(db, user.id)

    rows = (
        db.query(UserSkillProgress, Skill)
        .join(Skill, Skill.id == UserSkillProgress.skill_id)
        .filter(UserSkillProgress.user_id == user.id)
        .all()
    )
    skills = [
        SkillProgressItem(
            skill_id=skill.id,
            skill_title=skill.title,
            xp=progress.xp,
            completion_percent=progress.completion_percent,
            crowns=progress.crowns,
            completed=progress.completed,
        )
        for progress, skill in rows
    ]

    return ProgressResponse(
        user_id=user.id,
        xp=user.xp,
        streak=user.streak,
        hearts=user.hearts,
        gems=user.gems,
        daily_goal=user.daily_goal,
        daily_xp=daily_xp,
        daily_goal_reached=daily_xp >= user.daily_goal,
        skills=skills,
    )


@router.post("/practice", response_model=PracticeResponse)
def practice_refill(db: Session = Depends(get_db)) -> PracticeResponse:
    """Mocked practice/refill mechanism: restores the learner's hearts."""
    user = user_service.get_default_user(db)
    user = progress_service.practice_refill(db, user)
    return PracticeResponse(
        hearts=user.hearts,
        gems=user.gems,
        message="Hearts refilled via practice!",
    )
