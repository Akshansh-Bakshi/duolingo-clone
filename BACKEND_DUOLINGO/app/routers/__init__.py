"""
Aggregates all individual routers into a single `api_router` mounted
under the `/api` prefix in main.py. Adding a new resource means adding a
router module here and one `include_router` line — main.py itself never
needs to grow.
"""
from fastapi import APIRouter

from app.routers import courses, health, leaderboard, lessons, profile, progress, users

api_router = APIRouter()

# health check is intentionally NOT under /api — kept at the app root so
# it's reachable even if the API prefix changes.
health_router = health.router

api_router.include_router(users.router)
api_router.include_router(courses.router)
api_router.include_router(lessons.router)
api_router.include_router(progress.router)
api_router.include_router(profile.router)
api_router.include_router(leaderboard.router)
