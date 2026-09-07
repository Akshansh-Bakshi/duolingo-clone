"""
Seed system: populates a fresh database with the default learner, a few
extra seeded users (for a non-trivial leaderboard), and the full course
content tree (course -> units -> skills -> lessons -> exercises).

Idempotent: running it against an already-seeded database is a no-op
(it checks for existing data before inserting), so it's safe to run on
every app startup as well as manually via `python -m app.seed.seed_data`.

Usage:
    python -m app.seed.seed_data          # seed if empty
    python -m app.seed.seed_data --reset  # drop all tables and reseed
"""
from __future__ import annotations

import argparse
import sys

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import Base, SessionLocal, engine, init_db
from app.models import Course, Exercise, Lesson, Skill, Unit, User
from app.seed.course_content import COURSE

# A few extra learners so the leaderboard (spec: "may use seeded users")
# has more than one entry out of the box.
EXTRA_SEEDED_USERS = [
    {"username": "Maria", "xp": 340, "streak": 12},
    {"username": "Alex", "xp": 210, "streak": 4},
    {"username": "Priya", "xp": 95, "streak": 2},
]


def _course_already_seeded(db: Session) -> bool:
    return db.query(Course).first() is not None


def seed_course_content(db: Session) -> None:
    if _course_already_seeded(db):
        print("Course content already seeded — skipping.")
        return

    course = Course(
        name=COURSE["name"],
        source_language=COURSE["source_language"],
        target_language=COURSE["target_language"],
    )
    db.add(course)
    db.flush()  # assign course.id

    # Tracks the most recently created skill across the WHOLE course (not
    # reset per unit), so unlocking chains continue from one unit's last
    # skill into the next unit's first skill — only the very first skill
    # in the entire course has no prerequisite.
    previous_skill: Skill | None = None

    for unit_index, unit_data in enumerate(COURSE["units"]):
        unit = Unit(
            course_id=course.id,
            title=unit_data["title"],
            description=unit_data.get("description"),
            order_index=unit_index,
        )
        db.add(unit)
        db.flush()

        for skill_index, skill_data in enumerate(unit_data["skills"]):
            skill = Skill(
                unit_id=unit.id,
                title=skill_data["title"],
                description=skill_data.get("description"),
                order_index=skill_index,
                # Each skill unlocks after the previous one in the whole
                # course (cross-unit), matching spec section 11's example
                # progression. The very first skill has no prerequisite.
                required_skill_id=previous_skill.id if previous_skill else None,
            )
            db.add(skill)
            db.flush()

            for lesson_index, lesson_data in enumerate(skill_data["lessons"]):
                lesson = Lesson(
                    skill_id=skill.id,
                    title=lesson_data["title"],
                    order_index=lesson_index,
                )
                db.add(lesson)
                db.flush()

                for exercise_index, exercise_data in enumerate(lesson_data["exercises"]):
                    exercise = Exercise(
                        lesson_id=lesson.id,
                        type=exercise_data["type"],
                        question=exercise_data["question"],
                        correct_answer=exercise_data["correct_answer"],
                        options=exercise_data.get("options"),
                        data=exercise_data.get("data"),
                        order_index=exercise_index,
                    )
                    db.add(exercise)

            previous_skill = skill

    db.commit()
    print(f"Seeded course '{course.name}' with {len(COURSE['units'])} units.")


def seed_default_user(db: Session) -> None:
    existing = db.query(User).filter(User.username == settings.DEFAULT_USERNAME).first()
    if existing:
        print(f"Default user '{settings.DEFAULT_USERNAME}' already exists — skipping.")
        return

    user = User(
        username=settings.DEFAULT_USERNAME,
        xp=0,
        streak=0,
        hearts=settings.INITIAL_HEARTS,
        gems=settings.INITIAL_GEMS,
        daily_goal=settings.DEFAULT_DAILY_GOAL_XP,
    )
    db.add(user)
    db.commit()
    print(f"Seeded default user '{user.username}'.")


def seed_extra_users(db: Session) -> None:
    for data in EXTRA_SEEDED_USERS:
        existing = db.query(User).filter(User.username == data["username"]).first()
        if existing:
            continue
        db.add(
            User(
                username=data["username"],
                xp=data["xp"],
                streak=data["streak"],
                hearts=settings.INITIAL_HEARTS,
                gems=settings.INITIAL_GEMS,
                daily_goal=settings.DEFAULT_DAILY_GOAL_XP,
            )
        )
    db.commit()
    print("Seeded extra leaderboard users (if not already present).")


def run_seed(reset: bool = False) -> None:
    if reset:
        print("Dropping all tables (--reset)...")
        import app.models  # noqa: F401  (register models before drop/create)

        Base.metadata.drop_all(bind=engine)

    init_db()

    db = SessionLocal()
    try:
        seed_default_user(db)
        seed_extra_users(db)
        seed_course_content(db)
    finally:
        db.close()

    print("Seed complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed the Duolingo clone database.")
    parser.add_argument(
        "--reset", action="store_true", help="Drop all tables before seeding."
    )
    args = parser.parse_args(sys.argv[1:])
    run_seed(reset=args.reset)
