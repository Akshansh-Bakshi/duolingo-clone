from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict:
    """Basic liveness endpoint — used to verify the API process is up."""
    return {"status": "ok"}
