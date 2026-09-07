from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Exercise
from app.schemas.exercise import ExerciseSubmitRequest, ExerciseSubmitResponse
from app.schemas.lesson import (
    LessonCompleteRequest,
    LessonCompleteResponse,
    LessonDetailResponse,
)
from app.services import lesson_service, progress_service, user_service

router = APIRouter(prefix="/lessons", tags=["lessons"])


@router.get("/{lesson_id}", response_model=LessonDetailResponse)
def get_lesson(lesson_id: int, db: Session = Depends(get_db)) -> LessonDetailResponse:
    """Returns a lesson and its ordered exercises (without correct answers)."""
    lesson = lesson_service.get_lesson(db, lesson_id)
    if lesson is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")
    return LessonDetailResponse.model_validate(lesson)


@router.post("/{lesson_id}/submit", response_model=ExerciseSubmitResponse)
def submit_answer(
    lesson_id: int, body: ExerciseSubmitRequest, db: Session = Depends(get_db)
) -> ExerciseSubmitResponse:
    """
    Validates a single exercise answer. The backend is authoritative:
    on a wrong answer a heart is deducted server-side and the resulting
    heart count is returned so the frontend never has to guess.
    """
    lesson = lesson_service.get_lesson(db, lesson_id)
    if lesson is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")

    exercise = db.query(Exercise).filter(
        Exercise.id == body.exercise_id, Exercise.lesson_id == lesson_id
    ).first()
    if exercise is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found in this lesson",
        )

    user = user_service.get_default_user(db)

    try:
        is_correct, hearts_remaining, out_of_hearts = lesson_service.submit_answer(
            db, user, lesson, exercise, body.answer
        )
    except lesson_service.OutOfHeartsError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Out of hearts. Practice to refill before continuing.",
        )

    if is_correct:
        message = "Correct!"
    elif out_of_hearts:
        message = "Incorrect. Out of hearts!"
    else:
        message = "Incorrect. Try the next one."

    return ExerciseSubmitResponse(
        correct=is_correct,
        correct_answer=exercise.correct_answer,
        hearts_remaining=hearts_remaining,
        out_of_hearts=out_of_hearts,
        message=message,
    )


@router.post("/{lesson_id}/complete", response_model=LessonCompleteResponse)
def complete_lesson(
    lesson_id: int, body: LessonCompleteRequest, db: Session = Depends(get_db)
) -> LessonCompleteResponse:
    """
    Finalizes a lesson: awards XP, updates skill progress/crowns, daily
    activity, streak, and records the lesson attempt.
    """
    lesson = lesson_service.get_lesson(db, lesson_id)
    if lesson is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")

    total_exercises = len(lesson.exercises)
    if body.total_exercises != total_exercises:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"total_exercises ({body.total_exercises}) does not match the lesson's "
                f"actual exercise count ({total_exercises})"
            ),
        )
    if not (0 <= body.correct_count <= total_exercises):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="correct_count out of range for this lesson",
        )

    user = user_service.get_default_user(db)
    summary = progress_service.complete_lesson(
        db,
        user,
        lesson,
        correct_count=body.correct_count,
        total_exercises=total_exercises,
        hearts_lost=body.hearts_lost,
    )
    return LessonCompleteResponse(**summary)
