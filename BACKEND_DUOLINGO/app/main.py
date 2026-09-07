"""
FastAPI application entrypoint.

Wires together configuration, CORS, database initialization, and the
aggregated API router. Deliberately thin — no business logic lives here;
see app/services/ for that (routers → services → ORM/database).
"""
from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_db
from app.routers import api_router, health_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure tables exist on startup. This does NOT seed data — run
    # `python -m app.seed.seed_data` separately (see README) so seeding
    # stays an explicit, developer-controlled step rather than something
    # that silently happens on every restart.
    init_db()
    yield


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(api_router, prefix=settings.API_PREFIX)
