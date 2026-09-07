"use client";

// The lesson state machine described in ProjectSpecs.md section 12:
//   loading -> active -> (answer selected) -> submitting -> feedback
//   -> next exercise -> ... -> completing -> completed
// with an out_of_hearts branch that short-circuits to failure.
//
// The backend is authoritative for correctness, hearts, and XP — this hook
// only tracks transient, in-progress session state (current index, running
// correct count) exactly as FINAL_HANDOFF.md section 18 specifies.

import { useCallback, useEffect, useReducer, useRef } from "react";
import { api, ApiError } from "@/lib/api";
import type { CompleteResponse, Lesson, SubmitResponse } from "@/lib/types";

export type LessonPhase =
  | "loading"
  | "load_error"
  | "out_of_hearts"
  | "active"
  | "submitting"
  | "feedback"
  | "completing"
  | "complete_error"
  | "completed";

interface State {
  phase: LessonPhase;
  lesson: Lesson | null;
  currentIndex: number;
  selectedAnswer: string | null;
  correctCount: number;
  heartsLost: number;
  hearts: number;
  lastSubmit: SubmitResponse | null;
  completeResult: CompleteResponse | null;
  errorMessage: string | null;
}

type Action =
  | { type: "LOAD_START" }
  | { type: "LOAD_SUCCESS"; lesson: Lesson; hearts: number }
  | { type: "LOAD_ERROR"; message: string }
  | { type: "SET_ANSWER"; answer: string | null }
  | { type: "SUBMIT_START" }
  | { type: "SUBMIT_SUCCESS"; result: SubmitResponse }
  | { type: "SUBMIT_ERROR"; message: string }
  | { type: "CONTINUE" }
  | { type: "COMPLETE_START" }
  | { type: "COMPLETE_SUCCESS"; result: CompleteResponse }
  | { type: "COMPLETE_ERROR"; message: string }
  | { type: "REFILL_SUCCESS"; hearts: number };

const initialState: State = {
  phase: "loading",
  lesson: null,
  currentIndex: 0,
  selectedAnswer: null,
  correctCount: 0,
  heartsLost: 0,
  hearts: 5,
  lastSubmit: null,
  completeResult: null,
  errorMessage: null,
};

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case "LOAD_START":
      return { ...initialState, phase: "loading" };
    case "LOAD_ERROR":
      return { ...state, phase: "load_error", errorMessage: action.message };
    case "LOAD_SUCCESS":
      if (action.hearts <= 0) {
        return {
          ...state,
          phase: "out_of_hearts",
          lesson: action.lesson,
          hearts: 0,
        };
      }
      return {
        ...state,
        phase: "active",
        lesson: action.lesson,
        hearts: action.hearts,
        currentIndex: 0,
        selectedAnswer: null,
        correctCount: 0,
        heartsLost: 0,
      };
    case "SET_ANSWER":
      return { ...state, selectedAnswer: action.answer };
    case "SUBMIT_START":
      return { ...state, phase: "submitting" };
    case "SUBMIT_ERROR":
      return { ...state, phase: "active", errorMessage: action.message };
    case "SUBMIT_SUCCESS": {
      const { result } = action;
      const nextCorrectCount = result.correct
        ? state.correctCount + 1
        : state.correctCount;
      const nextHeartsLost = result.correct
        ? state.heartsLost
        : state.heartsLost + 1;
      return {
        ...state,
        phase: "feedback",
        lastSubmit: result,
        hearts: result.hearts_remaining,
        correctCount: nextCorrectCount,
        heartsLost: nextHeartsLost,
        errorMessage: null,
      };
    }
    case "CONTINUE": {
      if (state.lastSubmit?.out_of_hearts) {
        return { ...state, phase: "out_of_hearts" };
      }
      const isLast =
        state.lesson != null &&
        state.currentIndex >= state.lesson.exercises.length - 1;
      if (isLast) {
        return { ...state, phase: "completing" };
      }
      return {
        ...state,
        phase: "active",
        currentIndex: state.currentIndex + 1,
        selectedAnswer: null,
        lastSubmit: null,
      };
    }
    case "COMPLETE_START":
      return { ...state, phase: "completing" };
    case "COMPLETE_SUCCESS":
      return {
        ...state,
        phase: "completed",
        completeResult: action.result,
        hearts: action.result.hearts_remaining,
      };
    case "COMPLETE_ERROR":
      return { ...state, phase: "complete_error", errorMessage: action.message };
    case "REFILL_SUCCESS":
      return {
        ...state,
        phase: "active",
        hearts: action.hearts,
      };
    default:
      return state;
  }
}

export function useLessonPlayer(lessonId: number) {
  const [state, dispatch] = useReducer(reducer, initialState);
  // Guards the auto-fired /complete call against React StrictMode's
  // dev-only double-invocation of effects, which would otherwise award
  // XP/streak twice for a single lesson completion.
  const completeInFlight = useRef(false);

  const load = useCallback(async () => {
    dispatch({ type: "LOAD_START" });
    try {
      const [lesson, me] = await Promise.all([
        api.getLesson(lessonId),
        api.getMe(),
      ]);
      if (lesson.exercises.length === 0) {
        dispatch({
          type: "LOAD_ERROR",
          message: "This lesson has no exercises yet.",
        });
        return;
      }
      dispatch({ type: "LOAD_SUCCESS", lesson, hearts: me.hearts });
    } catch (err) {
      dispatch({
        type: "LOAD_ERROR",
        message:
          err instanceof ApiError ? err.detail : "Failed to load the lesson.",
      });
    }
  }, [lessonId]);

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [lessonId]);

  const setAnswer = useCallback((answer: string | null) => {
    dispatch({ type: "SET_ANSWER", answer });
  }, []);

  const submit = useCallback(async () => {
    if (!state.lesson || state.selectedAnswer == null || state.selectedAnswer === "")
      return;
    const exercise = state.lesson.exercises[state.currentIndex];
    dispatch({ type: "SUBMIT_START" });
    try {
      const result = await api.submitAnswer(lessonId, {
        exercise_id: exercise.id,
        answer: state.selectedAnswer,
      });
      dispatch({ type: "SUBMIT_SUCCESS", result });
    } catch (err) {
      if (err instanceof ApiError && err.status === 409) {
        dispatch({ type: "SUBMIT_SUCCESS", result: {
          correct: false,
          correct_answer: "",
          hearts_remaining: 0,
          out_of_hearts: true,
          message: err.detail,
        }});
        return;
      }
      dispatch({
        type: "SUBMIT_ERROR",
        message:
          err instanceof ApiError ? err.detail : "Failed to submit your answer.",
      });
    }
  }, [lessonId, state.lesson, state.selectedAnswer, state.currentIndex]);

  const continueNext = useCallback(() => {
    dispatch({ type: "CONTINUE" });
  }, []);

  const completeLesson = useCallback(async () => {
    if (!state.lesson) return;
    dispatch({ type: "COMPLETE_START" });
    try {
      const result = await api.completeLesson(lessonId, {
        correct_count: state.correctCount,
        total_exercises: state.lesson.exercises.length,
        hearts_lost: state.heartsLost,
      });
      dispatch({ type: "COMPLETE_SUCCESS", result });
    } catch (err) {
      completeInFlight.current = false;
      dispatch({
        type: "COMPLETE_ERROR",
        message:
          err instanceof ApiError ? err.detail : "Failed to finalize the lesson.",
      });
    }
  }, [lessonId, state.lesson, state.correctCount, state.heartsLost]);

  // Auto-fire the /complete call the moment the machine enters "completing".
  useEffect(() => {
    if (state.phase === "completing" && !state.completeResult && !completeInFlight.current) {
      completeInFlight.current = true;
      completeLesson();
    }
    if (state.phase !== "completing") {
      completeInFlight.current = false;
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [state.phase]);

  const retryComplete = useCallback(() => {
    completeInFlight.current = false;
    dispatch({ type: "COMPLETE_START" });
  }, []);

  // Errors are intentionally left to propagate so OutOfHearts can show a
  // local retry affordance instead of tearing down the whole screen.
  const refill = useCallback(async () => {
    const res = await api.practiceRefill();
    dispatch({ type: "REFILL_SUCCESS", hearts: res.hearts });
  }, []);

  return {
    state,
    actions: { load, setAnswer, submit, continueNext, refill, retryComplete },
  };
}
