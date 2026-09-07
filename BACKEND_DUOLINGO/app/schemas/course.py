from __future__ import annotations

import enum

from pydantic import BaseModel, ConfigDict


class CourseResponse(BaseModel):
    """Response item for GET /api/courses."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    source_language: str
    target_language: str


class SkillStatus(str, enum.Enum):
    LOCKED = "LOCKED"
    AVAILABLE = "AVAILABLE"
    COMPLETED = "COMPLETED"


class LessonSummary(BaseModel):
    """A lightweight lesson reference used within the path response."""

    id: int
    title: str
    order_index: int


class SkillPathItem(BaseModel):
    """A skill node as rendered on the learning path, with computed status/progress."""

    id: int
    title: str
    description: str | None
    order_index: int
    status: SkillStatus
    completion_percent: int
    crowns: int
    required_skill_id: int | None
    lessons: list[LessonSummary]


class UnitPathItem(BaseModel):
    """A unit section on the learning path, containing its skills."""

    id: int
    title: str
    description: str | None
    order_index: int
    skills: list[SkillPathItem]


class CoursePathResponse(BaseModel):
    """Response for GET /api/courses/{course_id}/path."""

    course_id: int
    course_name: str
    units: list[UnitPathItem]
