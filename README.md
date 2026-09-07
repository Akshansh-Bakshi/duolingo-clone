# Duolingo Web App Clone — SDE Fullstack Assignment

This repository contains the implementation for the Duolingo Web App clone
assignment described in `ProjectSpecs.md`.

## Repository Structure

```
duolingo_clone/
├── ProjectSpecs.md        Full assignment specification (source of truth)
├── README.md               This file
├── BACKEND_DUOLINGO/       FastAPI + SQLAlchemy + SQLite backend (complete)
└── FRONTEND_DUOLINGO/      Next.js frontend (not yet implemented)
```

## Status

- **Backend:** Complete. FastAPI application with full database schema,
  seed system, and all API endpoints required for the learning path,
  lesson player, and gamification mechanics. See
  `BACKEND_DUOLINGO/README.md` for setup instructions, architecture,
  database schema, API overview, and implementation assumptions.
- **Frontend:** Not yet implemented. `FRONTEND_DUOLINGO/` is currently a
  placeholder directory.

## Quick Start (Backend)

```bash
cd BACKEND_DUOLINGO
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.seed.seed_data
uvicorn app.main:app --reload --port 8000
```

Full details, including the database schema, API endpoint reference, and
documented assumptions (default learner, exercise-answer format), are in
`BACKEND_DUOLINGO/README.md`.

## Source of Truth

`ProjectSpecs.md` in this directory is the authoritative specification
this implementation follows. Where an implementation decision required
judgment beyond what the spec states explicitly, that decision is
documented in `BACKEND_DUOLINGO/README.md` under "Important Assumptions"
rather than silently assumed.
