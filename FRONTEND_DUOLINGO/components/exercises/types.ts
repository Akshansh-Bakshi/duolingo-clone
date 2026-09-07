import type { Exercise } from "@/lib/types";

export interface ExerciseFeedback {
  correct: boolean;
  correctAnswer: string;
}

export interface ExerciseComponentProps {
  exercise: Exercise;
  /** Current answer value, in the exact format the backend expects for this
   * exercise type (see FINAL_HANDOFF.md section 9). */
  value: string | null;
  onChange: (value: string) => void;
  /** True once submitted (submitting/feedback phases) — locks input. */
  disabled: boolean;
  /** Present only during the feedback phase; drives correct/incorrect styling. */
  feedback: ExerciseFeedback | null;
}
