from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.profile import ProfileResponse
from app.services import profile_service, user_service

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("", response_model=ProfileResponse)
def get_profile(db: Session = Depends(get_db)) -> ProfileResponse:
    """Returns the default learner's profile statistics."""
    user = user_service.get_default_user(db)
    data = profile_service.build_profile(db, user)
    return ProfileResponse(**data)
