// Shared TypeScript types mirroring FRONTEND_API_CONTRACT.md exactly.
// Keep this file in sync with the backend contract — do not invent fields.

export type SkillStatus = "LOCKED" | "AVAILABLE" | "COMPLETED";

export type ExerciseType =
  | "multiple_choice"
  | "translate"
  | "word_bank"
  | "match"
  | "fill_blank"
  | "type_answer";

export interface User {
  id: number;
  username: string;
  xp: number;
  streak: number;
  hearts: number;
  gems: number;
  daily_goal: number;
  daily_xp: number;
}

export interface Course {
  id: number;
  name: string;
  source_language: string;
  target_language: string;
}

export interface PathLesson {
  id: number;
  title: string;
  order_index: number;
}

export interface PathSkill {
  id: number;
  title: string;
  description: string;
  order_index: number;
  status: SkillStatus;
  completion_percent: number;
  crowns: number;
  required_skill_id: number | null;
  lessons: PathLesson[];
}

export interface PathUnit {
  id: number;
  title: string;
  description: string;
  order_index: number;
  skills: PathSkill[];
}

export interface CoursePath {
  course_id: number;
  course_name: string;
  units: PathUnit[];
}

export interface MatchPair {
  left: string;
  right: string;
}

export interface Exercise {
  id: number;
  lesson_id: number;
  type: ExerciseType;
  question: string;
  options: string[] | null;
  data: { pairs: MatchPair[] } | null;
  order_index: number;
}

export interface Lesson {
  id: number;
  skill_id: number;
  title: string;
  order_index: number;
  exercises: Exercise[];
}

export interface SubmitRequest {
  exercise_id: number;
  answer: string;
}

export interface SubmitResponse {
  correct: boolean;
  correct_answer: string;
  hearts_remaining: number;
  out_of_hearts: boolean;
  message: string;
}

export interface CompleteRequest {
  correct_count: number;
  total_exercises: number;
  hearts_lost: number;
}

export interface CompleteResponse {
  xp_earned: number;
  total_xp: number;
  perfect: boolean;
  skill_id: number;
  skill_completion_percent: number;
  skill_crowns: number;
  skill_completed: boolean;
  streak: number;
  daily_xp: number;
  daily_goal: number;
  daily_goal_reached: boolean;
  hearts_remaining: number;
}

export interface SkillProgress {
  skill_id: number;
  skill_title: string;
  xp: number;
  completion_percent: number;
  crowns: number;
  completed: boolean;
}

export interface Progress {
  user_id: number;
  xp: number;
  streak: number;
  hearts: number;
  gems: number;
  daily_goal: number;
  daily_xp: number;
  daily_goal_reached: boolean;
  skills: SkillProgress[];
}

export interface PracticeResponse {
  hearts: number;
  gems: number;
  message: string;
}

export interface Profile {
  username: string;
  total_xp: number;
  streak: number;
  hearts: number;
  gems: number;
  completed_skills: number;
  total_skills: number;
  lessons_completed: number;
}

export interface LeaderboardEntry {
  rank: number;
  username: string;
  xp: number;
}

export interface Leaderboard {
  entries: LeaderboardEntry[];
}

// Generic API error shape used across the app.
export interface ApiErrorPayload {
  status: number;
  detail: string;
}
