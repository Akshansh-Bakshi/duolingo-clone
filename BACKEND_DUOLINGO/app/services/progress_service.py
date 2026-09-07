"""
Business logic for gamification: XP awarding, streak updates, skill
progress/crowns, daily activity, and lesson completion recording.

This is the heart of spec section 11 ("Gamification Rules") and the
POST /api/lessons/{lesson_id}/complete flow from section 10.
"""
from __future__ import annotations

import datetime as dt

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import (
    DailyActivity,
    Lesson,
    LessonAttempt,
    Skill,
    User,
    UserSkillProgress,
)


def calculate_xp(correct_count: int, total_exercises: int) -> tuple[int, bool]:
    """
    Deterministic XP scoring (spec section 11):
      - perfect lesson (no mistakes): +30 XP
      - normal completion: +20 XP

    Returns (xp_earned, is_perfect).
    """
    is_perfect = total_exercises > 0 and correct_count == total_exercises
    xp = settings.XP_PERFECT_LESSON if is_perfect else settings.XP_LESSON_COMPLETE
    return xp, is_perfect


def update_streak(user: User, today: dt.date) -> int:
    """
    Update `user.streak` according to the rules in spec section 11:

      - no previous activity            -> streak = 1
      - last activity was yesterday     -> streak += 1
      - last activity was today already -> unchanged
      - last activity older than yesterday -> streak = 1 (reset)
    """
    last_date = user.last_activity.date() if user.last_activity else None

    if last_date == today:
        pass  # already recorded activity today; streak does not change again
    elif last_date == today - dt.timedelta(days=1):
        user.streak += 1
    else:
        # Covers both "no previous activity" and "lapsed streak" cases.
        user.streak = 1

    user.last_activity = dt.datetime.combine(today, dt.datetime.min.time())
    return user.streak


def record_daily_activity(db: Session, user_id: int, today: dt.date, xp_earned: int) -> DailyActivity:
    """Accumulate XP earned today into the (user, date) daily_activity row."""
    activity = (
        db.query(DailyActivity)
        .filter(DailyActivity.user_id == user_id, DailyActivity.activity_date == today)
        .first()
    )
    if activity is None:
        activity = DailyActivity(user_id=user_id, activity_date=today, xp_earned=0)
        db.add(activity)

    activity.xp_earned += xp_earned
    return activity


def update_skill_progress(db: Session, user: User, skill: Skill) -> UserSkillProgress:
    """
    Recompute a skill's completion_percent/crowns/completed flag from how
    many of its lessons have at least one completed LessonAttempt (spec
    section 11 "Skill Progress").
    """
    progress = (
        db.query(UserSkillProgress)
        .filter(UserSkillProgress.user_id == user.id, UserSkillProgress.skill_id == skill.id)
        .first()
    )
    if progress is None:
        progress = UserSkillProgress(user_id=user.id, skill_id=skill.id)
        db.add(progress)

    lesson_ids = [lesson.id for lesson in skill.lessons]
    total_lessons = len(lesson_ids)

    if total_lessons == 0:
        progress.completion_percent = 0
        progress.crowns = 0
        progress.completed = False
        return progress

    skill_attempts = (
        db.query(LessonAttempt)
        .filter(
            LessonAttempt.user_id == user.id,
            LessonAttempt.lesson_id.in_(lesson_ids),
            LessonAttempt.completed.is_(True),
        )
        .all()
    )
    completed_lesson_ids = {a.lesson_id for a in skill_attempts}
    completed_count = len(completed_lesson_ids)

    progress.completion_percent = round((completed_count / total_lessons) * 100)
    # Crowns scale 0-5 with completion, mirroring Duolingo's crown levels.
    progress.crowns = round((completed_count / total_lessons) * 5)
    progress.completed = completed_count >= total_lessons
    # Derived (not incremented) from every completed attempt on this
    # skill's lessons, so it stays consistent even if a lesson is
    # replayed rather than drifting from repeated += mutations.
    progress.xp = sum(a.xp_earned for a in skill_attempts)

    return progress


def complete_lesson(
    db: Session,
    user: User,
    lesson: Lesson,
    correct_count: int,
    total_exercises: int,
    hearts_lost: int,
) -> dict:
    """
    Orchestrates the full "finish a lesson" flow (spec section 10):
    calculate XP, update user XP, update skill progress, update daily
    activity, update streak, record the lesson attempt, and return a
    summary. Runs as a single DB transaction — commit happens once at the
    end so a failure partway through leaves nothing half-applied.
    """
    today = dt.datetime.utcnow().date()

    xp_earned, is_perfect = calculate_xp(correct_count, total_exercises)

    user.xp += xp_earned
    update_streak(user, today)

    activity = record_daily_activity(db, user.id, today, xp_earned)

    attempt = LessonAttempt(
        user_id=user.id,
        lesson_id=lesson.id,
        score=correct_count,
        xp_earned=xp_earned,
        hearts_lost=hearts_lost,
        completed=True,
        completed_at=dt.datetime.utcnow(),
    )
    db.add(attempt)
    # Flush so the attempt above is visible to the completed-lessons query
    # inside update_skill_progress (same transaction, not yet committed).
    db.flush()

    progress = update_skill_progress(db, user, lesson.skill)

    db.add(user)
    db.commit()
    db.refresh(user)
    db.refresh(progress)
    db.refresh(activity)

    return {
        "xp_earned": xp_earned,
        "total_xp": user.xp,
        "perfect": is_perfect,
        "skill_id": lesson.skill.id,
        "skill_completion_percent": progress.completion_percent,
        "skill_crowns": progress.crowns,
        "skill_completed": progress.completed,
        "streak": user.streak,
        "daily_xp": activity.xp_earned,
        "daily_goal": user.daily_goal,
        "daily_goal_reached": activity.xp_earned >= user.daily_goal,
        "hearts_remaining": user.hearts,
    }


def practice_refill(db: Session, user: User) -> User:
    """Mocked practice/refill mechanism (spec section 10/11): restores hearts."""
    user.hearts = min(settings.MAX_HEARTS, user.hearts + settings.PRACTICE_HEARTS_RESTORED)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
