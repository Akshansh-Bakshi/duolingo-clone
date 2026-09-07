from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Course
from app.schemas.course import CoursePathResponse, CourseResponse
from app.services import path_service, user_service

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("", response_model=list[CourseResponse])
def list_courses(db: Session = Depends(get_db)) -> list[CourseResponse]:
    """Returns all available courses (spec: one seeded English -> Spanish course)."""
    courses = db.query(Course).all()
    return [CourseResponse.model_validate(c) for c in courses]


@router.get("/{course_id}/path", response_model=CoursePathResponse)
def get_course_path(course_id: int, db: Session = Depends(get_db)) -> CoursePathResponse:
    """
    Returns the full learning path for a course: units -> skills -> lessons,
    with each skill's computed lock/unlock status, completion percentage,
    and crowns for the default learner.
    """
    user = user_service.get_default_user(db)
    path = path_service.build_course_path(db, course_id, user)
    if path is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return path
