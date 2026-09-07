# FRONTEND_DUOLINGO

Next.js (TypeScript, App Router) frontend for the Duolingo clone assignment.
Talks exclusively to the FastAPI backend described in `FRONTEND_API_CONTRACT.md` /
`FINAL_HANDOFF.md` from the project root — no mock/fake data.

## Tech stack

- Next.js 14 (App Router) + React 18 + TypeScript
- Plain CSS Modules (no UI framework) for a hand-built, Duolingo-inspired design system
- No client-side state library — a small `useReducer`-based state machine
  (`hooks/useLessonPlayer.ts`) drives the lesson player, and a React Context
  (`hooks/useUserContext.tsx`) holds the backend-authoritative gamification stats
  (streak/XP/hearts/gems) shared across pages

## Setup

```bash
cd FRONTEND_DUOLINGO
npm install
cp .env.local.example .env.local   # edit if your backend isn't on 127.0.0.1:8000
npm run dev
```

The app runs on http://localhost:3000 and expects the backend
(`BACKEND_DUOLINGO`) running at the URL in `NEXT_PUBLIC_API_BASE_URL`
(default `http://127.0.0.1:8000`). Start the backend first:

```bash
cd ../BACKEND_DUOLINGO
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m app.seed.seed_data
uvicorn app.main:app --reload --port 8000
```

Enable CORS on the backend for `http://localhost:3000` if it isn't already
(FastAPI's `CORSMiddleware`) — this frontend makes plain `fetch` calls from
the browser to the API base URL.

## Routes

| Route | Purpose |
|---|---|
| `/` | Redirects to `/learn` |
| `/learn` | Learning path — units, skills, lock/unlock, crowns, daily goal |
| `/lesson/[lessonId]` | Full-screen lesson player |
| `/profile` | Learner profile stats |
| `/leaderboard` | Seeded leaderboard |
| `/settings` | Placeholder page |

## Architecture

```
app/
  layout.tsx              Root HTML shell
  page.tsx                Redirect to /learn
  (main)/                 Route group sharing the app chrome (TopBar + SideNav)
    layout.tsx
    learn/page.tsx
    profile/page.tsx
    leaderboard/page.tsx
    settings/page.tsx
  lesson/[lessonId]/page.tsx   Full-screen, no shared chrome (matches Duolingo's
                                distraction-free lesson UX)

components/
  layout/       TopBar, SideNav, AppShell
  path/         LearningPath, UnitSection, SkillNode, DailyGoalCard
  lesson/       LessonPlayer, LessonHeader, FeedbackBar, LessonComplete, OutOfHearts
  exercises/    ExerciseRenderer + one component per exercise type
                (MultipleChoice, Translate, WordBank, MatchPairs, FillBlank, TypeAnswer)
  profile/      ProfileView
  leaderboard/  LeaderboardView
  common/       LoadingState / ErrorState / EmptyState

hooks/
  useLessonPlayer.ts   Lesson state machine (loading -> active -> submitting ->
                        feedback -> completing -> completed / out_of_hearts)
  useUserContext.tsx   Global gamification stats, backed by GET /api/users/me

lib/
  api.ts     Single API access layer — every backend call goes through here
  types.ts   TypeScript types mirroring FRONTEND_API_CONTRACT.md exactly
```

## Backend integration

Every endpoint in `FRONTEND_API_CONTRACT.md` is wired up via `lib/api.ts`:
`GET /health`, `GET /api/users/me`, `GET /api/courses`,
`GET /api/courses/{id}/path`, `GET /api/lessons/{id}`,
`POST /api/lessons/{id}/submit`, `POST /api/lessons/{id}/complete`,
`GET /api/progress`, `POST /api/progress/practice`, `GET /api/profile`,
`GET /api/leaderboard`.

The backend is treated as authoritative for everything it's documented to own:
answer correctness, hearts, XP, streak, crowns, skill status/progress, and
persistence. The frontend only tracks transient in-lesson session state
(current exercise index, running correct count) as called out in
`FINAL_HANDOFF.md` section 18, and never recomputes or overrides a backend
value.

## Known limitations / not implemented

- No automated frontend test suite (matches the backend's documented state —
  manual verification only).
- Hearts "regenerate over time" is not implemented; only the documented mocked
  `POST /api/progress/practice` refill exists, per the actual API contract.
- Achievements/badges, audio, dark mode, and timed practice are explicitly
  out of scope per `ProjectSpecs.md` section 19 (bonus/optional only) and were
  not built, to prioritize the mandatory lesson loop and gamification.
- This environment has no network access, so `npm install` / `npm run build`
  could not be executed here to produce a build log. The code was instead
  verified with a standalone `tsc --noEmit` pass against every source file
  (ignoring only the expected "cannot find module" noise from missing
  `node_modules`, e.g. `react`, `next`, and `*.module.css` ambient types,
  which Next.js resolves automatically once dependencies are installed).
  Run `npm install && npm run build` locally to get a full build log.
