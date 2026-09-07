# Duolingo Clone — Project Specification

## 1. Project Goal

Build a functional Duolingo-inspired language learning web application.

The application must reproduce the core Duolingo learning experience:

- Learning path / skill tree
- Units and skills
- Locked / available / completed progression
- Interactive lessons
- Multiple exercise types
- Immediate correct/incorrect feedback
- Hearts
- XP
- Streak
- Daily XP goal
- Skill progress
- Leaderboard
- Learner profile
- Persistent learner progress
- Playful, colorful, gamified UI
- Lesson completion and failure states

The focus is the lesson loop and gamification rather than large amounts of language content.

Use one seeded language course with a small amount of content.

Authentication may be simplified to a default logged-in learner.

Do NOT implement real payments, subscriptions, speech recognition, social networking, or multiple languages.

---

# 2. Required Technology Stack

## Frontend

- Next.js
- TypeScript
- React
- CSS / CSS Modules

## Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic

## Database

- SQLite

Do not introduce unnecessary frameworks or infrastructure.

---

# 3. Architecture

Use a simple full-stack architecture:

Browser
    ↓
Next.js Frontend
    ↓ HTTP/JSON REST API
FastAPI Backend
    ↓
Service / Business Logic
    ↓
SQLAlchemy ORM
    ↓
SQLite

## Separation of concerns

Frontend:
- UI rendering
- user interaction
- lesson-session state
- API communication
- animations and visual states

Backend:
- API endpoints
- validation
- answer checking
- XP calculation
- hearts
- streak logic
- skill progression
- persistence
- leaderboard/profile data

Database:
- course content
- learner data
- learner progress
- lesson history
- daily activity

Business logic should not be unnecessarily embedded directly inside API route handlers.

---

# 4. Repository Structure

Current repository:

duolingo_clone/
├── BACKEND_DUOLINGO/
├── FRONTEND_DUOLINGO/
├── ProjectSpecs.md
└── README.md

Backend target structure:

BACKEND_DUOLINGO/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   ├── models/
│   ├── schemas/
│   ├── routers/
│   ├── services/
│   └── seed/
├── tests/
├── requirements.txt
└── README.md

Frontend target structure:

FRONTEND_DUOLINGO/
├── app/
│   ├── page.tsx
│   ├── learn/
│   ├── lesson/
│   │   └── [lessonId]/
│   ├── profile/
│   ├── leaderboard/
│   └── settings/
├── components/
│   ├── layout/
│   ├── path/
│   ├── lesson/
│   ├── exercises/
│   ├── profile/
│   └── common/
├── hooks/
├── lib/
└── styles/

Exact file organization may be adjusted when necessary, but maintain clear separation of concerns and reusable components.

---

# 5. Database Schema

## users

Fields:

- id: INTEGER PRIMARY KEY
- username: TEXT UNIQUE
- xp: INTEGER
- streak: INTEGER
- hearts: INTEGER
- gems: INTEGER
- daily_goal: INTEGER
- last_activity: DATETIME
- created_at: DATETIME

---

## courses

Fields:

- id: INTEGER PRIMARY KEY
- name: TEXT
- source_language: TEXT
- target_language: TEXT

Relationship:

Course 1 → many Units

---

## units

Fields:

- id: INTEGER PRIMARY KEY
- course_id: FOREIGN KEY → courses.id
- title: TEXT
- description: TEXT
- order_index: INTEGER

Relationship:

Unit 1 → many Skills

---

## skills

Fields:

- id: INTEGER PRIMARY KEY
- unit_id: FOREIGN KEY → units.id
- title: TEXT
- description: TEXT
- order_index: INTEGER
- required_skill_id: FOREIGN KEY → skills.id, nullable

`required_skill_id` determines progression/unlocking.

Relationship:

Skill 1 → many Lessons

---

## lessons

Fields:

- id: INTEGER PRIMARY KEY
- skill_id: FOREIGN KEY → skills.id
- title: TEXT
- order_index: INTEGER

Relationship:

Lesson 1 → many Exercises

---

## exercises

Fields:

- id: INTEGER PRIMARY KEY
- lesson_id: FOREIGN KEY → lessons.id
- type: TEXT
- question: TEXT
- correct_answer: TEXT
- options: JSON/TEXT, nullable
- data: JSON/TEXT, nullable
- order_index: INTEGER

Supported exercise types:

- multiple_choice
- translate
- word_bank
- match
- fill_blank
- type_answer

Use `data` for exercise-specific structured information when required.

---

## user_skill_progress

Fields:

- id: INTEGER PRIMARY KEY
- user_id: FOREIGN KEY → users.id
- skill_id: FOREIGN KEY → skills.id
- xp: INTEGER
- completion_percent: INTEGER
- crowns: INTEGER
- completed: BOOLEAN
- updated_at: DATETIME

Unique constraint:

(user_id, skill_id)

---

## lesson_attempts

Fields:

- id: INTEGER PRIMARY KEY
- user_id: FOREIGN KEY → users.id
- lesson_id: FOREIGN KEY → lessons.id
- score: INTEGER
- xp_earned: INTEGER
- hearts_lost: INTEGER
- completed: BOOLEAN
- completed_at: DATETIME

---

## daily_activity

Fields:

- id: INTEGER PRIMARY KEY
- user_id: FOREIGN KEY → users.id
- activity_date: DATE
- xp_earned: INTEGER

Unique constraint:

(user_id, activity_date)

---

# 6. Database Relationships

Course
└── Units
    └── Skills
        └── Lessons
            └── Exercises

User
├── UserSkillProgress
├── LessonAttempts
└── DailyActivity

Skills may reference another Skill through `required_skill_id` to determine unlocking.

---

# 7. Default User

Real authentication is NOT required.

Use a seeded default learner.

Example:

username: Learner

The backend may assume the default learner/user ID for this assignment.

All learner-specific data must still be stored in the database and persist across refreshes/restarts.

---

# 8. Seed Data

Seed one language course:

English → Spanish

Suggested structure:

Unit 1: Basics

Skill 1: Greetings
- Greetings 1
- Greetings 2

Skill 2: Food
- Food 1
- Food 2

Skill 3: Everyday Words
- Everyday Words 1
- Everyday Words 2

Unit 2: Everyday Life

Skill 4: People
- People 1
- People 2

Skill 5: Home
- Home 1
- Home 2

Skill 6: Activities
- Activities 1
- Activities 2

The exact number may be adjusted for implementation speed.

Each lesson should contain approximately 6 exercises and collectively demonstrate ALL required exercise types.

---

# 9. Exercise Examples

## Multiple Choice

Question:
"What does hola mean?"

Options:
- Hello
- Goodbye
- Thank you
- Please

Correct answer:
Hello

## Translate

Question:
"Translate: Hello"

Correct answer:
Hola

## Word Bank

Question:
"Build: I eat bread"

Available words:
- Yo
- como
- pan

Correct:
Yo como pan

## Match

Pairs:

hello → hola
food → comida
water → agua

## Fill Blank

Question:
"Yo ___ pan."

Correct:
como

## Type Answer

Question:
"Translate: Thank you"

Correct:
gracias

---

# 10. Required REST API

Base prefix:

/api

## User

GET /api/users/me

Returns:

- id
- username
- xp
- streak
- hearts
- gems
- daily_goal
- daily_xp

---

## Courses

GET /api/courses

Returns available courses.

GET /api/courses/{course_id}/path

Returns the complete learning path including:

- units
- skills
- lessons
- skill status
- completion percentage
- crowns
- lock/unlock state

Skill states:

- LOCKED
- AVAILABLE
- COMPLETED

---

## Lessons

GET /api/lessons/{lesson_id}

Returns lesson information and its exercises.

POST /api/lessons/{lesson_id}/submit

Request contains:

- exercise_id
- answer

Backend validates the answer.

Response should contain enough information for the frontend to display:

- correct/incorrect
- correct answer when appropriate
- hearts remaining
- relevant feedback

The backend is authoritative for answer validation.

POST /api/lessons/{lesson_id}/complete

When the lesson is successfully completed:

- calculate XP
- update user XP
- update skill progress
- update daily activity
- update streak
- record lesson attempt
- return lesson completion summary

---

## Progress

GET /api/progress

Returns learner progress.

POST /api/progress/practice

Provides a mocked practice/refill mechanism for hearts.

---

## Profile

GET /api/profile

Returns:

- username
- total XP
- streak
- completed skills
- achievements/statistics where implemented

---

## Leaderboard

GET /api/leaderboard

Returns users ordered by XP.

Leaderboard may use seeded users.

---

# 11. Gamification Rules

## Hearts

Initial hearts:

5

Wrong answer:

hearts = hearts - 1

Minimum:

0

When hearts reach 0:

- stop the lesson
- show Out of Hearts state/modal

Provide a mocked practice/refill mechanism to restore hearts.

---

## XP

Use simple deterministic scoring.

Recommended:

Normal lesson completion:
+20 XP

Perfect lesson:
+30 XP total

XP should be awarded on successful lesson completion rather than for every individual answer.

---

## Skill Progress

Skill progress is determined from completed lessons within that skill.

Example:

4 lessons:

Lesson 1 complete → 25%
Lesson 2 complete → 50%
Lesson 3 complete → 75%
Lesson 4 complete → 100%

At 100%:

skill = completed

The next required skill becomes available.

---

## Skill Unlocking

Initial state:

Skill 1 → AVAILABLE
Skill 2 → LOCKED
Skill 3 → LOCKED

After completing Skill 1:

Skill 1 → COMPLETED
Skill 2 → AVAILABLE
Skill 3 → LOCKED

Continue based on `required_skill_id`.

---

## Streak

Activity qualifies the learner for that day.

Rules:

No previous activity:
streak = 1

Activity yesterday + activity today:
streak += 1

Previous activity older than yesterday:
streak = 1

Activity already recorded today:
streak does not increase again

Daily activity must be persisted.

---

## Daily Goal

Default:

50 XP

Track today's XP and display progress such as:

30 / 50 XP

When the goal is reached, show a celebration state.

---

# 12. Lesson State Machine

Lesson states:

- loading
- active
- feedback
- completing
- completed
- failed

Flow:

START
↓
LOADING
↓
ACTIVE
↓
ANSWER SELECTED
↓
CORRECT / INCORRECT
↓
SHOW FEEDBACK
↓
NEXT EXERCISE
↓
ACTIVE
↓
all exercises complete
↓
COMPLETING
↓
LESSON COMPLETE
↓
XP + PROGRESS + STREAK
↓
RETURN TO PATH

If hearts reach zero:

ACTIVE
↓
INCORRECT
↓
HEARTS = 0
↓
OUT OF HEARTS
↓
FAILED

---

# 13. Frontend Routes

## /

Redirect to /learn.

---

## /learn

Main Duolingo-style learning path.

Must contain:

- top bar
- streak
- XP
- hearts
- gems
- units
- skills
- locked state
- available state
- completed state
- progress indicators
- lesson entry points

---

## /lesson/[lessonId]

Lesson player.

Must contain:

- back/navigation control
- lesson progress bar
- heart counter
- current exercise
- answer interaction
- feedback bar
- continue button
- completion modal
- out-of-hearts state

---

## /profile

Display:

- learner name
- XP
- streak
- completed skills
- statistics
- achievements if implemented

---

## /leaderboard

Display seeded leaderboard sorted by XP.

---

## /settings

Simple placeholder page.

No complex settings system required.

---

# 14. Frontend Component Architecture

## Layout

- TopBar
- Navigation

## Learning Path

- LearningPath
- UnitSection
- SkillNode

SkillNode should receive:

- title
- status
- completion
- crowns
- lesson information

---

## Lesson

- LessonPlayer
- LessonProgress
- HeartCounter
- ExerciseRenderer
- FeedbackBar
- LessonComplete
- OutOfHearts

---

## Exercises

- MultipleChoice
- Translate
- WordBank
- MatchPairs
- FillBlank
- TypeAnswer

`ExerciseRenderer` selects the correct exercise component based on exercise type.

Exercise components should be reusable and independently understandable.

---

# 15. UI/UX Requirements

The application must feel like a polished modern language-learning game rather than a generic quiz application.

Visual priorities:

1. Learning path
2. Lesson player
3. Correct/incorrect feedback
4. Top navigation/gamification
5. Progress indicators
6. Completion/failure states
7. Profile
8. Leaderboard
9. Settings

Use:

- playful colorful visual language
- rounded components
- strong visual hierarchy
- prominent primary buttons
- progress indicators
- skill nodes
- cards
- animations/transitions
- celebratory states
- feedback states
- responsive layout

The UI should be strongly inspired by Duolingo's current interaction patterns, while remaining original implementation work.

Do not copy source code or assets from existing repositories.

---

# 16. Persistence Requirements

The following must persist in SQLite:

- XP
- streak
- hearts
- gems
- completed skills
- skill progress
- lesson attempts
- daily activity

Refreshing the page must not reset learner progress.

Restarting the backend must not reset learner progress unless the developer explicitly runs the seed/reset operation.

---

# 17. Error Handling

Use sensible HTTP status codes.

Examples:

200:
successful request

400:
invalid request/answer

404:
resource not found

409:
invalid state/conflict where appropriate

500:
unexpected server error

Frontend must display user-friendly error states rather than raw backend errors.

---

# 18. Implementation Order

Follow this order.

## Phase 1 — Foundation

- initialize Next.js frontend
- initialize FastAPI backend
- configure SQLite
- configure SQLAlchemy
- configure CORS
- establish folder structure
- establish configuration

## Phase 2 — Database

- create models
- create relationships
- create database initialization
- create seed system
- seed default user
- seed course content
- verify database

## Phase 3 — Backend

Implement:

- user endpoint
- course endpoint
- learning path endpoint
- lesson endpoint
- answer submission
- lesson completion
- progress
- profile
- leaderboard
- practice/refill

## Phase 4 — Frontend Foundation

Implement:

- routes
- API client
- shared TypeScript types
- global layout
- top navigation

## Phase 5 — Learning Path

Implement:

- units
- skills
- lock/unlock states
- completed states
- progress indicators
- lesson navigation

## Phase 6 — Lesson Player

Implement:

- lesson state machine
- exercise renderer
- multiple choice
- translate
- word bank
- match pairs
- fill blank
- type answer
- answer submission
- feedback
- lesson progress
- hearts
- completion
- failure

## Phase 7 — Gamification

Integrate:

- XP
- streak
- daily goal
- hearts
- skill progress
- leaderboard
- profile

## Phase 8 — UI Polish

Prioritize:

- spacing
- typography
- colors
- buttons
- skill nodes
- progress rings
- feedback bars
- animations
- completion modal
- out-of-hearts modal
- responsive behavior

## Phase 9 — Testing

Verify the complete flow:

Learn
→ Skill
→ Lesson
→ Correct answer
→ Incorrect answer
→ Heart loss
→ Finish lesson
→ XP awarded
→ Skill progress updated
→ Streak updated
→ Return to path
→ Refresh
→ Progress persists

Also test:

- zero hearts
- locked skill
- invalid lesson
- invalid exercise
- incorrect answer
- completed skill
- repeated activity on same day

## Phase 10 — Deployment

- public GitHub repository
- deploy backend
- deploy frontend
- configure production API URL
- verify CORS
- verify production database
- test complete deployed user flow
- finalize README

---

# 19. Scope Control

Do NOT spend significant time on:

- real authentication
- payments
- subscriptions
- speech recognition
- multiple languages
- social networking
- complex notification systems
- microservices
- unnecessary external infrastructure

Optional features only after all mandatory functionality is stable:

- achievements/badges
- audio
- functional leaderboard across users
- timed practice
- legendary mode
- dark mode
- advanced responsive behavior

---

# 20. Quality Requirements

The implementation must prioritize:

1. Functionality
2. Lesson loop correctness
3. Gamification correctness
4. UI/UX quality
5. Database quality
6. API design
7. Code readability
8. Component/service modularity
9. Persistence
10. Deployment stability

Avoid:

- duplicate functionality
- unnecessary dependencies
- frontend-only fake data where API data exists
- business logic duplicated between frontend and backend
- giant monolithic components
- giant monolithic API route files
- unnecessary abstraction
- undocumented assumptions

All submitted code should be understandable and explainable by the developer.

---

# 21. Definition of Done

The application is considered complete when a learner can:

1. Open the application
2. View the learning path
3. See locked and unlocked skills
4. Enter an available lesson
5. Complete all required exercise types
6. Receive immediate correct/incorrect feedback
7. Lose hearts on incorrect answers
8. Reach an out-of-hearts state
9. Complete a lesson
10. Receive XP
11. Update skill progress
12. Update streak
13. Update daily goal
14. View profile statistics
15. View leaderboard
16. Return to the learning path
17. Refresh the application
18. See their progress still persisted

The deployed application and public GitHub repository must both work.
