# Duolingo Clone — Backend

FastAPI + SQLAlchemy + SQLite backend for the Duolingo clone assignment.
Implements the learning path, lesson player, and gamification API described
in `ProjectSpecs.md`.

## 1. Tech Stack

- **Framework:** FastAPI
- **ORM:** SQLAlchemy 2.0 (declarative models, typed `Mapped[...]` columns)
- **Validation / serialization:** Pydantic v2
- **Database:** SQLite (file-based, `duolingo.db`)
- **Server:** Uvicorn

No auth framework, task queue, cache, or second database — intentionally
out of scope per the assignment.

## 2. Setup Instructions

```bash
cd BACKEND_DUOLINGO

# create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate      # on Windows: .venv\Scripts\activate

# install dependencies
pip install -r requirements.txt

# seed the database (creates duolingo.db, tables, and course content)
python -m app.seed.seed_data

# run the API
uvicorn app.main:app --reload --port 8000
```

The API is now available at `http://127.0.0.1:8000`, with interactive
docs at `http://127.0.0.1:8000/docs`.

### Re-seeding / resetting

```bash
python -m app.seed.seed_data           # idempotent: no-op if already seeded
python -m app.seed.seed_data --reset   # drops all tables and reseeds from scratch
```

Running the app itself (`uvicorn app.main:app`) only ever calls
`create_all()` on startup — it never seeds data on its own. Seeding is a
deliberate, separate developer step, so restarting the server never
resets learner progress (per spec section 16).

### Environment variables (all optional, sensible defaults apply)

| Variable         | Default                                      | Purpose                          |
|------------------|-----------------------------------------------|-----------------------------------|
| `DATABASE_URL`   | `sqlite:///<repo>/duolingo.db`               | SQLAlchemy connection string      |
| `CORS_ORIGINS`   | `http://localhost:3000,http://127.0.0.1:3000` | Comma-separated allowed origins   |
| `DEFAULT_USERNAME` | `Learner`                                   | Username of the seeded default learner |
| `DEBUG`          | `true`                                        | Reserved for future use           |

## 3. Architecture

```
Browser / Next.js frontend
        │  HTTP/JSON
        ▼
FastAPI routers        (app/routers/*)   — request/response only, no business logic
        │
        ▼
Services                (app/services/*)  — business logic: XP, streak, hearts,
        │                                   skill progression, validation
        ▼
SQLAlchemy ORM models   (app/models/*)
        │
        ▼
SQLite (duolingo.db)
```

Strict layering: **routers → services → ORM/database**. Routers depend on
`get_db` (a FastAPI dependency yielding a SQLAlchemy `Session`) and call
into services; services own all business rules and are the only layer
that touches multiple models or makes decisions; models are plain data +
relationships with no logic of their own.

### Directory layout

```
BACKEND_DUOLINGO/
├── app/
│   ├── main.py              FastAPI app, CORS, router mounting, startup table creation
│   ├── core/
│   │   ├── config.py        Settings (env vars, gamification constants)
│   │   └── database.py      Engine, SessionLocal, Base, get_db, init_db
│   ├── models/               One file per table (see schema below)
│   ├── schemas/              Pydantic request/response models
│   ├── routers/               One file per resource; api_router aggregates them
│   ├── services/              Business logic (one module per concern)
│   └── seed/
│       ├── course_content.py  Static seed data (units/skills/lessons/exercises)
│       └── seed_data.py       Seeding script (idempotent + --reset)
├── tests/
├── requirements.txt
└── README.md
```

## 4. Database Schema

Matches `ProjectSpecs.md` section 5 exactly. SQLite file: `duolingo.db`.

| Table                 | Key columns                                                                 | Notes |
|------------------------|------------------------------------------------------------------------------|-------|
| `users`                | xp, streak, hearts, gems, daily_goal, last_activity                          | One row per learner (default learner + a few seeded leaderboard users) |
| `courses`              | name, source_language, target_language                                      | 1 → many `units` |
| `units`                | course_id (FK), title, order_index                                          | 1 → many `skills` |
| `skills`               | unit_id (FK), order_index, **required_skill_id (FK → skills.id, nullable)** | Self-referential FK drives lock/unlock. 1 → many `lessons` |
| `lessons`              | skill_id (FK), order_index                                                   | 1 → many `exercises` |
| `exercises`            | lesson_id (FK), type, question, correct_answer, options (JSON), data (JSON) | `correct_answer` is never sent to the client before submission |
| `user_skill_progress`  | user_id + skill_id (**unique**), xp, completion_percent, crowns, completed   | One row per (user, skill) |
| `lesson_attempts`      | user_id (FK), lesson_id (FK), score, xp_earned, hearts_lost, completed       | Audit trail; used to derive skill progress |
| `daily_activity`       | user_id + activity_date (**unique**), xp_earned                              | Source of truth for streak + daily goal |

Relationships:

```
Course → Units → Skills → Lessons → Exercises
User → UserSkillProgress
User → LessonAttempt
User → DailyActivity
Skill.required_skill_id → Skill.id   (self-referential, nullable)
```

`Skill.required_skill` and `.progress_entries` are ORM relationships
declared in `app/models/skill.py`; the self-referential FK uses
`remote_side=[id]` so SQLAlchemy can resolve the parent/child direction.

## 5. API Overview

All routes are mounted under `/api` (plus a root-level `/health`).

| Method | Path                                | Purpose |
|--------|--------------------------------------|---------|
| GET    | `/health`                            | Liveness check |
| GET    | `/api/users/me`                      | Default learner's stats + today's XP |
| GET    | `/api/courses`                       | List available courses |
| GET    | `/api/courses/{course_id}/path`      | Full units→skills→lessons tree with computed lock/unlock status, completion %, crowns |
| GET    | `/api/lessons/{lesson_id}`           | Lesson + its exercises (no answers) |
| POST   | `/api/lessons/{lesson_id}/submit`    | Validate one exercise answer; deducts a heart on wrong answers; 409 if already at 0 hearts |
| POST   | `/api/lessons/{lesson_id}/complete`  | Finalize a lesson: XP, skill progress/crowns, daily activity, streak, lesson attempt record |
| GET    | `/api/progress`                      | Overall + per-skill progress for the learner |
| POST   | `/api/progress/practice`             | Mocked hearts refill |
| GET    | `/api/profile`                       | Username, total XP, streak, completed skills, lessons completed |
| GET    | `/api/leaderboard`                   | Users ordered by XP, descending |

Interactive docs (request/response schemas, try-it-out): `/docs` (Swagger UI)
or `/redoc`.

### Error handling

- `404` — lesson/course/exercise not found
- `400` — `complete` request doesn't match the lesson's actual exercise count, or `correct_count` out of range
- `409` — submitting an answer while at 0 hearts (must practice/refill first)
- `500` — unexpected server error (e.g. seed step not run yet)

## 6. Seeded Content

One course, **Spanish for English Speakers** (English → Spanish):

- **Unit 1: Basics** — Greetings, Food, Everyday Words (3 skills)
- **Unit 2: Everyday Life** — People, Home, Activities (3 skills)
- Each skill has 2 lessons; each lesson has 6 exercises (72 exercises total)
- Every exercise type from the spec appears repeatedly: `multiple_choice`,
  `translate`, `word_bank`, `match`, `fill_blank`, `type_answer`

Skill unlocking is a single chain across the **whole course** (not just
within a unit): only the first skill (`Greetings`) starts `AVAILABLE`;
every other skill's `required_skill_id` points to the previous skill in
course order, including across the unit boundary (`People` requires
`Everyday Words`, the last skill of Unit 1).

Four users are seeded: the default learner (`Learner`, 0 XP) plus three
extra users (`Maria`, `Alex`, `Priya`) purely so `/api/leaderboard` has
more than one entry out of the box.

## 7. Important Assumptions

- **Default learner / no real auth.** Per spec section 7, there is no
  login. Every endpoint operates on behalf of a single seeded user
  (`username = "Learner"`, configurable via `DEFAULT_USERNAME`). The
  backend looks this user up by username on every request rather than
  taking a user ID from the client.
- **Answer comparison is a normalized string match.** All six exercise
  types store `correct_answer` as a single canonical string. Submitted
  answers are compared case-insensitively with whitespace collapsed
  (`" Hola "` == `"hola"`), but otherwise must match exactly. This keeps
  `check_answer()` type-agnostic instead of branching per exercise type.
- **`match` exercises use a canonical joined string as `correct_answer`**,
  e.g. `"hello-hola,goodbye-adios,please-por favor"`, while the actual
  pairs for rendering live in the `data` JSON field
  (`{"pairs": [{"left": ..., "right": ...}, ...]}`). The frontend is
  expected to submit the same canonical, comma-joined `"left-right"`
  format once all pairs are matched. This is a simplification documented
  here rather than a per-type answer schema, to keep the submit endpoint
  and `Exercise` model simple.
- **XP is awarded once per lesson**, not per exercise (spec section 11):
  20 XP normally, 30 XP if every exercise in that submission was correct
  (`correct_count == total_exercises`).
- **The `/complete` endpoint trusts but verifies.** The frontend reports
  `correct_count`/`total_exercises`/`hearts_lost` from its session state
  (since the live exercise-by-exercise session lives entirely on the
  frontend per the architecture split in spec section 3), but the backend
  rejects any `total_exercises` that doesn't match the lesson's actual
  exercise count, and any `correct_count` outside `[0, total_exercises]`.
  It does not re-derive correctness from individual `/submit` calls,
  since the spec doesn't require the backend to track an in-progress
  session between submit calls (only the running heart count).
- **Skill progress (`completion_percent`, `crowns`, `completed`, and the
  per-skill `xp`) is entirely derived**, not incrementally mutated. On
  every `/complete` call it's recomputed from the full set of that user's
  completed `lesson_attempts` rows for that skill's lessons. This means
  replaying an already-completed lesson doesn't double-count completion
  or crowns, and per-skill `xp` is always the true sum of XP earned from
  that skill's lessons.
- **Crowns scale 0–5** based on `completed_lessons / total_lessons`,
  mirroring Duolingo's crown levels (not specified numerically in the
  assignment, so a linear 0–5 scale was chosen as the simplest faithful
  interpretation).
- **Streak** is derived from `User.last_activity` + `daily_activity`
  rows, following the exact rules in spec section 11 (reset to 1 with no
  prior activity or a lapsed streak, +1 for consecutive-day activity, no
  change if already active today).
- **CORS** defaults to allowing `http://localhost:3000` (the expected
  Next.js dev server origin); override with `CORS_ORIGINS` for other
  environments.

## 8. Known Limitations / Remaining Work

- No automated test suite yet (`tests/` exists but is empty) — all
  verification so far has been manual, via the running server and direct
  SQLite inspection.
- No pagination on `/api/leaderboard` (fine at seed-data scale; add a
  `limit`/`offset` if the seeded user count grows significantly).
- No rate limiting or request logging beyond Uvicorn's access log.
