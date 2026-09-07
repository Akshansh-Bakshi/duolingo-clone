# FRONTEND_API_CONTRACT.md

Base URL: `http://127.0.0.1:8000` (dev). All endpoints below except `/health` are mounted under `/api`. All responses are JSON. No authentication — every request operates on the single seeded default learner (`username = "Learner"`).

---

## GET /health

**Purpose:** Liveness check.

**Request:** none.

**Response `200`:**
```json
{ "status": "ok" }
```

**Errors:** none expected.

**Frontend behavior:** Use only for connectivity/monitoring checks, not part of the app flow.

---

## GET /api/users/me

**Purpose:** Fetch the default learner's current top-bar stats (streak, XP, hearts, gems) plus today's XP progress.

**Request:** none.

**Response `200`:**
```json
{
  "id": 1,
  "username": "Learner",
  "xp": 30,
  "streak": 1,
  "hearts": 4,
  "gems": 500,
  "daily_goal": 50,
  "daily_xp": 30
}
```

**Important fields:**
- `daily_xp` is computed (today's accumulated XP), not a stored user column — use it with `daily_goal` to render the daily-goal progress ring.
- `hearts` is the live, authoritative heart count.

**Errors:** `500` if the seed script has never been run (no default user exists).

**Frontend behavior:** Call on app load / top-bar mount to populate streak, XP, hearts, gems, and daily goal progress.

---

## GET /api/courses

**Purpose:** List available courses (currently always exactly one seeded course).

**Request:** none.

**Response `200`:**
```json
[
  {
    "id": 1,
    "name": "Spanish for English Speakers",
    "source_language": "English",
    "target_language": "Spanish"
  }
]
```

**Errors:** none expected.

**Frontend behavior:** Use to populate a course selector, or just take the first (only) entry to drive the home path.

---

## GET /api/courses/{course_id}/path

**Purpose:** Fetch the full learning path (units → skills → lessons) with server-computed lock/unlock status and progress for the default learner. This is the primary data source for the Duolingo home screen.

**Request:** path param `course_id` (int).

**Response `200`:**
```json
{
  "course_id": 1,
  "course_name": "Spanish for English Speakers",
  "units": [
    {
      "id": 1,
      "title": "Basics",
      "description": "Greetings, food, and everyday words.",
      "order_index": 0,
      "skills": [
        {
          "id": 1,
          "title": "Greetings",
          "description": "Say hello and goodbye.",
          "order_index": 0,
          "status": "COMPLETED",
          "completion_percent": 100,
          "crowns": 5,
          "required_skill_id": null,
          "lessons": [
            { "id": 1, "title": "Greetings 1", "order_index": 0 },
            { "id": 2, "title": "Greetings 2", "order_index": 1 }
          ]
        }
      ]
    }
  ]
}
```

**Important fields:**
- `status`: one of `"LOCKED" | "AVAILABLE" | "COMPLETED"` — always server-computed; never derive this on the client.
- `completion_percent` / `crowns`: per-skill progress; `crowns` is 0–5.
- `required_skill_id`: informational only (which skill must be completed first); the frontend doesn't need to evaluate this itself since `status` already reflects it.

**Errors:** `404` if `course_id` doesn't exist.

**Frontend behavior:** Render the unit/skill tree; disable interaction on `LOCKED` skills; show crown/completion visuals per `crowns`/`completion_percent`; tapping a skill's lesson navigates to the lesson player using the lesson `id`.

---

## GET /api/lessons/{lesson_id}

**Purpose:** Fetch a lesson's ordered exercises to run the lesson player.

**Request:** path param `lesson_id` (int).

**Response `200`:**
```json
{
  "id": 1,
  "skill_id": 1,
  "title": "Greetings 1",
  "order_index": 0,
  "exercises": [
    {
      "id": 1,
      "lesson_id": 1,
      "type": "multiple_choice",
      "question": "What does 'hola' mean?",
      "options": ["Hello", "Goodbye", "Thank you", "Please"],
      "data": null,
      "order_index": 0
    }
  ]
}
```

**Important fields:**
- `type`: one of `multiple_choice | translate | word_bank | match | fill_blank | type_answer` — drives which exercise UI component to render.
- `options`: array, used by `multiple_choice` and `word_bank` (word tokens); `null` for other types.
- `data`: structured payload used by `match` exercises — `{"pairs": [{"left": "...", "right": "..."}]}`; `null` otherwise.
- **`correct_answer` is intentionally never included** — do not expect it in this response.

**Errors:** `404` if the lesson doesn't exist.

**Frontend behavior:** Render `exercises` in `order_index` order as the lesson session; keep local session state (current index, running correct count) entirely client-side; call `/submit` for each answer and `/complete` at the end.

---

## POST /api/lessons/{lesson_id}/submit

**Purpose:** Validate a single exercise answer. Authoritative for correctness and heart deduction.

**Request body:**
```json
{
  "exercise_id": 2,
  "answer": "Hola"
}
```

**Response `200` (correct):**
```json
{
  "correct": true,
  "correct_answer": "Hola",
  "hearts_remaining": 4,
  "out_of_hearts": false,
  "message": "Correct!"
}
```

**Response `200` (incorrect):**
```json
{
  "correct": false,
  "correct_answer": "Hola",
  "hearts_remaining": 3,
  "out_of_hearts": false,
  "message": "Incorrect. Try the next one."
}
```

**Response `200` (incorrect, hits 0 hearts):**
```json
{
  "correct": false,
  "correct_answer": "Buenos dias",
  "hearts_remaining": 0,
  "out_of_hearts": true,
  "message": "Incorrect. Out of hearts!"
}
```

**Important fields:**
- `correct_answer` is always returned (even on a correct submission) — use it to show the feedback bar's answer reveal.
- `hearts_remaining` is the live, authoritative heart count — sync local UI state to this value, don't decrement locally.
- `out_of_hearts` becomes `true` on the exact submission that brings hearts to 0.

**Errors:**
- `404` — lesson not found, or `exercise_id` doesn't belong to `lesson_id`.
- `409` — user already has 0 hearts; body: `{"detail": "Out of hearts. Practice to refill before continuing."}`.

**Frontend behavior:**
- On `correct: true` → show correct feedback, advance to next exercise.
- On `correct: false` → show incorrect feedback with `correct_answer`, decrement the hearts UI to `hearts_remaining`.
- On `out_of_hearts: true` or a `409` response → stop the lesson, show the "out of hearts" modal, and route toward practice/refill (`POST /api/progress/practice`) rather than allowing further submissions.

---

## POST /api/lessons/{lesson_id}/complete

**Purpose:** Finalize a lesson session: award XP, update skill progress/crowns, update streak and daily activity, record the lesson attempt.

**Request body:**
```json
{
  "correct_count": 6,
  "total_exercises": 6,
  "hearts_lost": 1
}
```
- `correct_count`: how many exercises the learner got right this session (frontend-tracked).
- `total_exercises`: must exactly equal the lesson's actual exercise count (from `GET /api/lessons/{id}`'s `exercises` array length) or the request is rejected.
- `hearts_lost`: optional, defaults to `0`; recorded for history only (does not affect the user's current heart count — hearts are only changed via `/submit` and `/practice`).

**Response `200`:**
```json
{
  "xp_earned": 30,
  "total_xp": 30,
  "perfect": true,
  "skill_id": 1,
  "skill_completion_percent": 50,
  "skill_crowns": 2,
  "skill_completed": false,
  "streak": 1,
  "daily_xp": 30,
  "daily_goal": 50,
  "daily_goal_reached": false,
  "hearts_remaining": 4
}
```

**Important fields:**
- `xp_earned`: 30 if perfect (`correct_count == total_exercises`), else 20.
- `skill_completion_percent` / `skill_crowns` / `skill_completed`: updated state for the skill this lesson belongs to — use to refresh the path view.
- `streak`: updated streak count — use to refresh the top bar.
- `daily_goal_reached`: whether today's XP now meets `daily_goal` — trigger the daily-goal-reached celebration if this flips to `true`.
- `hearts_remaining`: current hearts (unaffected by this call, but returned for convenience so the frontend can refresh the top bar in one response).

**Errors:**
- `404` — lesson not found.
- `400` — `total_exercises` doesn't match the lesson's actual exercise count, or `correct_count` is outside `[0, total_exercises]`.

**Frontend behavior:** Call once when the lesson session ends (all exercises answered or hearts hit 0 and player exits). Show the lesson-complete summary modal using this response directly — don't recompute XP/crowns client-side. Refresh the path view (or re-fetch `GET /api/courses/{id}/path`) afterward so newly unlocked skills appear.

---

## GET /api/progress

**Purpose:** Fetch overall + per-skill progress for the learner — useful for a dashboard or to refresh path/top-bar state without a full path re-fetch.

**Request:** none.

**Response `200`:**
```json
{
  "user_id": 1,
  "xp": 30,
  "streak": 1,
  "hearts": 4,
  "gems": 500,
  "daily_goal": 50,
  "daily_xp": 30,
  "daily_goal_reached": false,
  "skills": [
    {
      "skill_id": 1,
      "skill_title": "Greetings",
      "xp": 30,
      "completion_percent": 50,
      "crowns": 2,
      "completed": false
    }
  ]
}
```

**Important fields:** `skills` only includes skills the learner has at least started (has a `UserSkillProgress` row) — skills never attempted are absent from this list (they'd show as `LOCKED`/`AVAILABLE` with 0 progress in the `/path` response instead).

**Errors:** `500` if default user missing (seed not run).

**Frontend behavior:** Use for a profile/stats view or to sync top-bar + per-skill progress in one call.

---

## POST /api/progress/practice

**Purpose:** Mocked practice/refill mechanism — restores hearts.

**Request:** none (empty body).

**Response `200`:**
```json
{
  "hearts": 5,
  "gems": 500,
  "message": "Hearts refilled via practice!"
}
```

**Important fields:** `hearts` is the new, post-refill heart count (capped at 5).

**Errors:** `500` if default user missing.

**Frontend behavior:** Call from the "out of hearts" modal's practice/refill action; on success, update the hearts UI and allow the learner to resume/restart the lesson.

---

## GET /api/profile

**Purpose:** Learner profile page stats.

**Request:** none.

**Response `200`:**
```json
{
  "username": "Learner",
  "total_xp": 30,
  "streak": 1,
  "hearts": 4,
  "gems": 500,
  "completed_skills": 0,
  "total_skills": 6,
  "lessons_completed": 1
}
```

**Errors:** `500` if default user missing.

**Frontend behavior:** Render directly on the profile page — all fields are final display values, no client-side computation needed.

---

## GET /api/leaderboard

**Purpose:** Seeded leaderboard, ordered by XP descending.

**Request:** none. (No query params currently supported; returns up to 20 entries.)

**Response `200`:**
```json
{
  "entries": [
    { "rank": 1, "username": "Maria", "xp": 340 },
    { "rank": 2, "username": "Alex", "xp": 210 },
    { "rank": 3, "username": "Priya", "xp": 95 },
    { "rank": 4, "username": "Learner", "xp": 30 }
  ]
}
```

**Important fields:** `rank` is pre-computed (1-indexed, ties broken by query order) — do not re-sort or re-rank client-side.

**Errors:** none expected.

**Frontend behavior:** Render directly as the leaderboard list; highlight the row where `username === "Learner"` as the current user.
