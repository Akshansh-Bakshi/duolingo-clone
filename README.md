# 🦉 Duolingo Web App Clone

A full-stack Duolingo-inspired language learning web application built for an **SDE Full Stack Assignment**.

The project recreates the core Duolingo learning experience with an interactive learning path, lessons, multiple exercise types, XP, hearts, streaks, crowns, daily goals, progress tracking, and a leaderboard.

The application is split into a **Next.js frontend** and a **FastAPI backend**, with the backend acting as the source of truth for learning progress and gamification.

---

## 🚀 Live Demo

### Frontend
👉 https://duolingofrontend.vercel.app

### Backend API
👉 https://duolingo-clone-azpp.onrender.com

### API Documentation
👉 https://duolingo-clone-azpp.onrender.com/docs

### Health Check
👉 https://duolingo-clone-azpp.onrender.com/health

---

## ✨ Features

### 📚 Learning Experience
- Spanish for English Speakers course
- Structured learning path
- Units → Skills → Lessons → Exercises
- Skill locking and unlocking
- Skill completion percentage
- Crown progression
- Daily XP goal

### 🧠 Interactive Lessons
Six exercise types are implemented:

- Multiple Choice
- Translation
- Word Bank
- Match Pairs
- Fill in the Blank
- Type Answer

Each lesson contains multiple exercises and provides immediate feedback.

### 🎮 Gamification
- XP system
- Hearts system
- Streak tracking
- Gems
- Daily XP goal
- Skill crowns
- Leaderboard
- Lesson completion tracking

### 📊 Progress Tracking
The backend persists:

- Lesson attempts
- XP earned
- Hearts lost
- Skill completion
- Crown levels
- Daily activity
- Streak information

### 🏆 Leaderboard
A seeded leaderboard ranks learners by total XP.

The default learner is accompanied by seeded users so the leaderboard has meaningful entries immediately after setup.

---

# 🏗️ Architecture

```text
                         ┌──────────────────────┐
                         │      Browser         │
                         │   Next.js Frontend   │
                         └──────────┬───────────┘
                                    │
                              HTTP / JSON
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      FastAPI         │
                         │      REST API        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      Services        │
                         │  Business Logic      │
                         │ XP / Hearts / Streak │
                         │ Progress / Validation│
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     SQLAlchemy       │
                         │         ORM          │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       SQLite         │
                         │     duolingo.db      │
                         └──────────────────────┘
