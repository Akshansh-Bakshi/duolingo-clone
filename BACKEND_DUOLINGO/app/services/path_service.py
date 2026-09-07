"""
Business logic for the learning path (spec section 10 "Courses" +
section 11 "Skill Unlocking").

A skill's status is derived, not stored:

- COMPLETED: the user's UserSkillProgress row for that skill has
  completed = True.
- AVAILABLE: not completed, and either it has no `required_skill_id`
  (first skill in the course) or its required skill is completed.
- LOCKED: not completed, and its required skill is not yet completed.
"""
from __future__ import annotations

from sqlalchemy.orm import Session, joinedload

from app.models import Course, Skill, Unit, User, UserSkillProgress
from app.schemas.course import (
    CoursePathResponse,
    LessonSummary,
    SkillPathItem,
    SkillStatus,
    UnitPathItem,
)


def _progress_map(db: Session, user_id: int) -> dict[int, UserSkillProgress]:
    rows = db.query(UserSkillProgress).filter(UserSkillProgress.user_id == user_id).all()
    return {row.skill_id: row for row in rows}


def compute_skill_status(
    skill: Skill, progress_by_skill: dict[int, UserSkillProgress]
) -> SkillStatus:
    progress = progress_by_skill.get(skill.id)
    if progress and progress.completed:
        return SkillStatus.COMPLETED

    if skill.required_skill_id is None:
        return SkillStatus.AVAILABLE

    required_progress = progress_by_skill.get(skill.required_skill_id)
    if required_progress and required_progress.completed:
        return SkillStatus.AVAILABLE

    return SkillStatus.LOCKED


def build_course_path(db: Session, course_id: int, user: User) -> CoursePathResponse | None:
    """Assemble the full units -> skills -> lessons tree with computed status/progress."""
    course = (
        db.query(Course)
        .options(joinedload(Course.units).joinedload(Unit.skills).joinedload(Skill.lessons))
        .filter(Course.id == course_id)
        .first()
    )
    if course is None:
        return None

    progress_by_skill = _progress_map(db, user.id)

    unit_items: list[UnitPathItem] = []
    for unit in sorted(course.units, key=lambda u: u.order_index):
        skill_items: list[SkillPathItem] = []
        for skill in sorted(unit.skills, key=lambda s: s.order_index):
            progress = progress_by_skill.get(skill.id)
            status = compute_skill_status(skill, progress_by_skill)
            skill_items.append(
                SkillPathItem(
                    id=skill.id,
                    title=skill.title,
                    description=skill.description,
                    order_index=skill.order_index,
                    status=status,
                    completion_percent=progress.completion_percent if progress else 0,
                    crowns=progress.crowns if progress else 0,
                    required_skill_id=skill.required_skill_id,
                    lessons=[
                        LessonSummary(id=l.id, title=l.title, order_index=l.order_index)
                        for l in sorted(skill.lessons, key=lambda x: x.order_index)
                    ],
                )
            )
        unit_items.append(
            UnitPathItem(
                id=unit.id,
                title=unit.title,
                description=unit.description,
                order_index=unit.order_index,
                skills=skill_items,
            )
        )

    return CoursePathResponse(course_id=course.id, course_name=course.name, units=unit_items)
