"""Business logic for the learner profile page (spec section 10 "Profile")."""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.models import LessonAttempt, Skill, User, UserSkillProgress


def build_profile(db: Session, user: User) -> dict:
    total_skills = db.query(Skill).count()
    completed_skills = (
        db.query(UserSkillProgress)
        .filter(UserSkillProgress.user_id == user.id, UserSkillProgress.completed.is_(True))
        .count()
    )
    lessons_completed = (
        db.query(LessonAttempt.lesson_id)
        .filter(LessonAttempt.user_id == user.id, LessonAttempt.completed.is_(True))
        .distinct()
        .count()
    )

    return {
        "username": user.username,
        "total_xp": user.xp,
        "streak": user.streak,
        "hearts": user.hearts,
        "gems": user.gems,
        "completed_skills": completed_skills,
        "total_skills": total_skills,
        "lessons_completed": lessons_completed,
    }
