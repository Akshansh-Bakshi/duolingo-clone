"use client";

import { useMemo } from "react";
import { useLessonPlayer } from "@/hooks/useLessonPlayer";
import ExerciseRenderer from "@/components/exercises/ExerciseRenderer";
import LessonHeader from "./LessonHeader";
import FeedbackBar from "./FeedbackBar";
import LessonComplete from "./LessonComplete";
import OutOfHearts from "./OutOfHearts";
import { LoadingState, ErrorState } from "@/components/common/StateViews";
import styles from "./LessonPlayer.module.css";

export default function LessonPlayer({ lessonId }: { lessonId: number }) {
  const { state, actions } = useLessonPlayer(lessonId);

  const exercise = useMemo(() => {
    if (!state.lesson) return null;
    return state.lesson.exercises[state.currentIndex] ?? null;
  }, [state.lesson, state.currentIndex]);

  if (state.phase === "loading") {
    return <LoadingState label="Loading lesson..." />;
  }

  if (state.phase === "load_error") {
    return (
      <ErrorState
        message={state.errorMessage ?? "Failed to load the lesson."}
        onRetry={actions.load}
      />
    );
  }

  if (state.phase === "out_of_hearts") {
    return <OutOfHearts onRefill={actions.refill} />;
  }

  if (state.phase === "completing" && !state.completeResult) {
    return <LoadingState label="Saving your progress..." />;
  }

  if (state.phase === "complete_error") {
    return (
      <ErrorState
        title="Couldn't save your progress"
        message={state.errorMessage ?? "Something went wrong finishing the lesson."}
        onRetry={actions.retryComplete}
      />
    );
  }

  if (state.phase === "completed" && state.completeResult) {
    return <LessonComplete result={state.completeResult} />;
  }

  if (!state.lesson || !exercise) {
    return <LoadingState label="Loading lesson..." />;
  }

  const isFeedback = state.phase === "feedback";
  const isSubmitting = state.phase === "submitting";
  const canCheck =
    state.phase === "active" &&
    state.selectedAnswer != null &&
    state.selectedAnswer.trim() !== "";

  const feedback =
    isFeedback && state.lastSubmit
      ? {
          correct: state.lastSubmit.correct,
          correctAnswer: state.lastSubmit.correct_answer,
        }
      : null;

  return (
    <div className={styles.page}>
      <LessonHeader
        current={state.currentIndex + (isFeedback ? 1 : 0)}
        total={state.lesson.exercises.length}
        hearts={state.hearts}
      />

      <div className={styles.body}>
        {state.errorMessage && state.phase === "active" && (
          <p style={{ color: "var(--color-red)", marginBottom: 16, fontSize: 14 }}>
            {state.errorMessage}
          </p>
        )}
        <ExerciseRenderer
          key={exercise.id}
          exercise={exercise}
          value={state.selectedAnswer}
          onChange={actions.setAnswer}
          disabled={isFeedback || isSubmitting}
          feedback={feedback}
        />
      </div>

      {!isFeedback && (
        <div className={styles.footer}>
          <div className={styles.footerInner}>
            <button
              className={`btn btn-primary ${styles.checkBtn}`}
              disabled={!canCheck || isSubmitting}
              onClick={actions.submit}
            >
              {isSubmitting ? "Checking..." : "Check"}
            </button>
          </div>
        </div>
      )}

      {isFeedback && state.lastSubmit && (
        <FeedbackBar
          correct={state.lastSubmit.correct}
          correctAnswer={state.lastSubmit.correct_answer}
          message={state.lastSubmit.message}
          onContinue={actions.continueNext}
        />
      )}
    </div>
  );
}
