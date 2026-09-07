# FINAL_HANDOFF.md

## 1. Current Project Tree

```
duolingo_clone/
├── ProjectSpecs.md
├── README.md
├── BACKEND_DUOLINGO/
│   ├── README.md
│   ├── requirements.txt
│   ├── duolingo.db
│   ├── app/
│   │   ├── main.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── database.py
│   │   ├── models/
│   │   │   ├── course.py
│   │   │   ├── daily_activity.py
│   │   │   ├── exercise.py
│   │   │   ├── lesson.py
│   │   │   ├── lesson_attempt.py
│   │   │   ├── skill.py
│   │   │   ├── unit.py
│   │   │   ├── user.py
│   │   │   └── user_skill_progress.py
│   │   ├── schemas/
│   │   │   ├── course.py
│   │   │   ├── exercise.py
│   │   │   ├── lesson.py
│   │   │   ├── profile.py
│   │   │   ├── progress.py
│   │   │   └── user.py
│   │   ├── routers/
│   │   │   ├── courses.py
│   │   │   ├── health.py
│   │   │   ├── leaderboard.py
│   │   │   ├── lessons.py
│   │   │   ├── profile.py
│   │   │   ├── progress.py
│   │   │   └── users.py
│   │   ├── services/
│   │   │   ├── leaderboard_service.py
│   │   │   ├── lesson_service.py
│   │   │   ├── path_service.py
│   │   │   ├── profile_service.py
│   │   │   ├── progress_service.py
│   │   │   └── user_service.py
│   │   └── seed/
│   │       ├── course_content.py
│   │       └── seed_data.py
│   └── tests/
└── FRONTEND_DUOLINGO/   (empty placeholder — not yet implemented)
```

## 2. Backend Entry Point and Startup Command

Entry point: `BACKEND_DUOLINGO/app/main.py` (FastAPI app instance: `app`)

```bash
cd BACKEND_DUOLINGO
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m app.seed.seed_data
uvicorn app.main:app --reload --port 8000
```

## 3. Frontend Entry Point

None. `FRONTEND_DUOLINGO/` is an empty placeholder directory. No frontend code exists yet.

## 4. Dependencies

Python (`BACKEND_DUOLINGO/requirements.txt`):
```
fastapi==0.115.6
uvicorn[standard]==0.32.1
sqlalchemy==2.0.36
pydantic==2.10.3
python-multipart==0.0.19
```

Node/frontend: none yet — no `package.json` exists.

## 5. Database Location

`BACKEND_DUOLINGO/duolingo.db` (SQLite file). Path is configurable via the `DATABASE_URL` env var (default: `sqlite:///<repo>/duolingo.db`).

## 6. Seed Command

```bash
python -m app.seed.seed_data           # idempotent — no-op if already seeded
python -m app.seed.seed_data --reset   # drops all tables and reseeds from scratch
```
Run from inside `BACKEND_DUOLINGO/`. Starting the server (`uvicorn app.main:app`) only creates tables if missing — it never seeds data itself.

## 7. Exact API Endpoint List

All under `/api` except `/health`:

- `GET /health`
- `GET /api/users/me`
- `GET /api/courses`
- `GET /api/courses/{course_id}/path`
- `GET /api/lessons/{lesson_id}`
- `POST /api/lessons/{lesson_id}/submit`
- `POST /api/lessons/{lesson_id}/complete`
- `GET /api/progress`
- `POST /api/progress/practice`
- `GET /api/profile`
- `GET /api/leaderboard`

Full request/response detail: see `FRONTEND_API_CONTRACT.md`.

## 8. Request/Response Behavior Relevant to the Frontend

- The backend operates on a single default learner (`username = "Learner"`); no auth, no user ID is passed by the client.
- `GET /api/lessons/{id}` never includes `correct_answer` — the client cannot see answers ahead of submission.
- `POST /.../submit` is authoritative for correctness and hearts: a wrong answer deducts a heart server-side; the response's `hearts_remaining` is the source of truth.
- At 0 hearts, `POST /.../submit` returns `409` instead of processing the answer — the frontend must block further submission and prompt practice/refill.
- `POST /.../complete` validates `total_exercises` against the lesson's actual exercise count (`400` on mismatch) and `correct_count` range (`400` if outside `[0, total_exercises]`).
- Skill `status` (`LOCKED` / `AVAILABLE` / `COMPLETED`) in the path response is always server-computed, never stored/sent by the client.

## 9. All Six Exercise Types and Answer Formats

All types store `correct_answer` as a single string, compared case-insensitively with whitespace collapsed.

| Type              | `question` example              | `options`/`data` example                                             | `correct_answer` format |
|-------------------|----------------------------------|------------------------------------------------------------------------|--------------------------|
| `multiple_choice` | "What does 'hola' mean?"        | `options`: `["Hello","Goodbye","Thank you","Please"]`                  | one option string, e.g. `"Hello"` |
| `translate`       | "Translate: Hello"              | none                                                                    | target-language string, e.g. `"Hola"` |
| `word_bank`       | "Build: Good morning"           | `options`: list of word tokens, e.g. `["Buenos","dias","noches","tardes"]` | full assembled phrase, e.g. `"Buenos dias"` |
| `fill_blank`      | "___ dias (Good day)"           | none                                                                    | the missing word, e.g. `"Buenos"` |
| `type_answer`     | "Translate: Goodbye"            | none                                                                    | free-typed string, e.g. `"Adios"` |
| `match`           | "Match the pairs"               | `data`: `{"pairs":[{"left":"hello","right":"hola"}, ...]}`             | canonical comma-joined string of all pairs: `"hello-hola,goodbye-adios,please-por favor"` — the frontend must submit this same joined format once all pairs are matched |

## 10. XP Rules

- Awarded once per lesson at `/complete`, not per exercise.
- Perfect lesson (`correct_count == total_exercises`, and `total_exercises > 0`): **30 XP**.
- Any other completion: **20 XP**.
- Added to `User.xp` and to that day's `daily_activity.xp_earned`.

## 11. Heart Rules

- Learner starts with 5 hearts (`INITIAL_HEARTS = 5`), max 5 (`MAX_HEARTS = 5`).
- Wrong answer on `/submit` → heart deducted (floor 0).
- Correct answer → no change.
- At 0 hearts, further `/submit` calls return `409` and do not process the answer.
- `POST /api/progress/practice` (mocked refill) restores hearts by `PRACTICE_HEARTS_RESTORED = 5`, capped at `MAX_HEARTS`.
- Hearts are unaffected by `/complete`.

## 12. Streak Rules

Based on `User.last_activity` (updated only via `/complete`) compared to the current UTC date:

- No prior activity → streak = 1.
- Last activity was yesterday → streak += 1.
- Last activity was already today → streak unchanged.
- Last activity older than yesterday (lapsed) → streak resets to 1.

## 13. Crown / Skill-Progress Rules

- `UserSkillProgress` (per user+skill) is fully **derived**, recomputed on every `/complete` call from that user's completed `lesson_attempts` for that skill's lessons — never incrementally mutated.
- `completion_percent = round(completed_lessons / total_lessons * 100)`.
- `crowns = round(completed_lessons / total_lessons * 5)` (0–5 scale).
- `completed = True` once all of the skill's lessons have at least one completed attempt.
- Per-skill `xp` = sum of `xp_earned` across all completed attempts for that skill's lessons.

## 14. Lesson Locking/Unlocking Rules

- Each `Skill.required_skill_id` points to the previous skill in course order (nullable for the very first skill).
- Unlock chain spans the **entire course**, not just within a unit — the first skill of unit 2 requires the last skill of unit 1.
- Computed status (never stored):
  - `COMPLETED` if that skill's `UserSkillProgress.completed = True`.
  - `AVAILABLE` if not completed, and (`required_skill_id` is null OR the required skill is completed).
  - `LOCKED` otherwise.

## 15. Current Seeded Data Counts

(As verified at handoff time — includes lesson progress from a completed manual test, described in section 16.)

| Table | Count |
|---|---|
| users | 4 |
| courses | 1 |
| units | 2 |
| skills | 6 |
| lessons | 12 |
| exercises | 72 |
| user_skill_progress | 1 |
| lesson_attempts | 1 |
| daily_activity | 1 |

Seeded users: `Learner` (default learner, currently xp=30/streak=1/hearts=4 from prior verification), `Maria` (340 xp), `Alex` (210 xp), `Priya` (95 xp).

Running `python -m app.seed.seed_data --reset` returns everything to a pristine state: `Learner` at xp=0/streak=0/hearts=5, and 0 rows in `user_skill_progress`/`lesson_attempts`/`daily_activity`.

## 16. Verification/Tests That Have Actually Passed

All performed manually against the running server (no automated test suite exists):

- Database creation and seeded row counts (course/unit/skill/lesson/exercise) verified correct.
- Schema constraints verified directly in SQLite: `uq_user_skill`, `uq_user_date` unique constraints, `required_skill_id` self-referential FK.
- `GET /api/users/me`, `GET /api/courses` — correct output.
- `GET /api/courses/{id}/path` — correct lock/unlock cascade across unit boundaries (after fix, see section 17).
- `GET /api/lessons/{id}` — correct exercises, `correct_answer` excluded; 404 on missing lesson.
- `POST /.../submit` — correct-answer path, wrong-answer heart deduction, zero-hearts trigger (`out_of_hearts: true`), and `409` on submitting again at 0 hearts.
- `POST /api/progress/practice` — hearts restored to 5.
- `POST /.../complete` — perfect (30 XP) vs normal (20 XP) scoring; skill completion %, crowns, `skill_completed` flag; streak; daily XP/goal — all verified correct on a clean database.
- Input validation on `/complete`: mismatched `total_exercises` → 400; out-of-range `correct_count` → 400; nonexistent lesson → 404.
- Streak logic unit-tested in isolation for all 4 rules (no prior activity, consecutive day, lapsed, same-day-twice).
- `GET /api/leaderboard`, `GET /api/profile`, `GET /api/progress` — correct output.
- **Full restart-persistence test**: completed a lesson, recorded XP/streak/hearts/skill progress/lesson history, fully killed the server process (confirmed via process list), verified data on disk independently, restarted the server (new process), and confirmed every value via the API matched exactly, including the derived path lock/unlock state.
- Seed script idempotency: re-running `python -m app.seed.seed_data` without `--reset` produces no duplicate rows and no-ops each seeding step.
- At handoff: backend module imports cleanly (`import app.main`), seed re-run idempotent, `/health` and `/api/users/me` respond correctly, persisted state from the prior verification pass is intact.

## 17. Known Limitations That Genuinely Remain

- No automated test suite — `tests/` directory exists but is empty; all verification has been manual.
- No pagination on `GET /api/leaderboard` (returns up to 20 users; fine at current seed scale).
- No rate limiting or structured request logging beyond Uvicorn's default access log.
- No frontend implementation exists yet.
- `duolingo.db` included in this handoff currently holds state from manual verification testing (one completed lesson for `Learner`), not a pristine seed. Run `python -m app.seed.seed_data --reset` for a clean slate.

## 18. Assumptions the Frontend Developer Must Know

- **No authentication.** Every request implicitly operates on the single seeded `Learner` user. There is no login flow, no user ID/token to pass.
- **Backend is authoritative for hearts and correctness.** The frontend should not locally decrement hearts or judge correctness — always use the `submit` response's `correct`, `hearts_remaining`, and `out_of_hearts` fields.
- **The in-progress lesson session (current exercise index, running correct count) lives entirely on the frontend.** The backend has no concept of "lesson in progress" between individual `/submit` calls — it only tracks the live heart count on the user. The frontend must accumulate `correct_count` itself and pass it to `/complete` at the end.
- **`/complete` must be called with the lesson's true exercise count** or it returns 400 — the frontend should use the `exercises` array length from `GET /api/lessons/{id}`, not a hardcoded number.
- **`match` exercises require the frontend to submit a canonical joined string** (`"left-right,left-right,..."`) as the answer once all pairs are matched — see section 9. This is a simplification, not a per-pair submission API.
- **Gems are present in `User`/response schemas but not actually spent or earned anywhere in current backend logic** — they are a static seeded value (500) with no purchase/reward endpoint implemented (matches spec's "gems can be mocked").
- **Crown scale is 0–5**, linear with lesson completion fraction — not explicitly specified in the assignment, so treat it as an interpretation, not a fixed external standard.
