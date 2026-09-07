"use client";

import { useState } from "react";
import type { ExerciseComponentProps } from "./types";
import styles from "./exercises.module.css";

/**
 * Tap-the-words exercise. The backend expects the fully assembled phrase
 * as a single space-joined string (FINAL_HANDOFF.md section 9), so this
 * component tracks the order tokens were tapped and reports the joined
 * string via onChange every time the selection changes.
 *
 * Token *indices* (not just strings) are tracked so duplicate words behave
 * correctly.
 */
export default function WordBank({
  exercise,
  onChange,
  disabled,
  feedback,
}: ExerciseComponentProps) {
  const options = exercise.options ?? [];
  const [usedIndices, setUsedIndices] = useState<number[]>([]);

  const emit = (indices: number[]) => {
    onChange(indices.map((i) => options[i]).join(" "));
  };

  const selectToken = (idx: number) => {
    if (disabled) return;
    const next = [...usedIndices, idx];
    setUsedIndices(next);
    emit(next);
  };

  const removeToken = (position: number) => {
    if (disabled) return;
    const next = usedIndices.filter((_, i) => i !== position);
    setUsedIndices(next);
    emit(next);
  };

  const availableSlots = options
    .map((tok, i) => ({ tok, i }))
    .filter(({ i }) => !usedIndices.includes(i));

  let stripCls = styles.answerStrip;

  return (
    <div>
      <p className={styles.prompt}>{exercise.question}</p>

      <div
        className={stripCls}
        style={
          feedback
            ? {
                borderBottomColor: feedback.correct
                  ? "var(--color-green)"
                  : "var(--color-red)",
              }
            : undefined
        }
      >
        {usedIndices.length === 0 && (
          <span style={{ color: "var(--color-text-faint)", fontSize: 14 }}>
            Tap the words below
          </span>
        )}
        {usedIndices.map((idx, position) => (
          <button
            key={`${idx}-${position}`}
            type="button"
            className={styles.wordChip}
            disabled={disabled}
            onClick={() => removeToken(position)}
          >
            {options[idx]}
          </button>
        ))}
      </div>

      <div className={styles.wordBankRow}>
        {availableSlots.map(({ tok, i }) => (
          <button
            key={i}
            type="button"
            className={styles.wordChipButton}
            disabled={disabled}
            onClick={() => selectToken(i)}
          >
            {tok}
          </button>
        ))}
      </div>

      {feedback && !feedback.correct && (
        <p style={{ marginTop: 16, fontSize: 14, color: "var(--color-text-soft)" }}>
          Correct answer: <strong>{feedback.correctAnswer}</strong>
        </p>
      )}
    </div>
  );
}
