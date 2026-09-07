"""
All ORM models, re-exported here so other modules can do
`from app.models import User, Course, ...` instead of reaching into
individual files. Importing this module also registers every model on
`Base.metadata`, which is required before `Base.metadata.create_all()`
(see app/core/database.py::init_db) will create all tables.
"""
from app.models.course import Course
from app.models.daily_activity import DailyActivity
from app.models.exercise import Exercise, ExerciseType
from app.models.lesson import Lesson
from app.models.lesson_attempt import LessonAttempt
from app.models.skill import Skill
from app.models.unit import Unit
from app.models.user import User
from app.models.user_skill_progress import UserSkillProgress

__all__ = [
    "Course",
    "DailyActivity",
    "Exercise",
    "ExerciseType",
    "Lesson",
    "LessonAttempt",
    "Skill",
    "Unit",
    "User",
    "UserSkillProgress",
]
