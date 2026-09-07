"use client";

import type { ExerciseComponentProps } from "./types";
import styles from "./exercises.module.css";

/** Fill-in-the-blank exercise, e.g. "Yo ___ pan." -> "como". */
export default function FillBlank({
  exercise,
  value,
  onChange,
  disabled,
  feedback,
}: ExerciseComponentProps) {
  let inputCls = styles.textInput;
  if (feedback) {
    inputCls += feedback.correct
      ? ` ${styles.textInputCorrect}`
      : ` ${styles.textInputIncorrect}`;
  }

  return (
    <div>
      <p className={styles.prompt}>{exercise.question}</p>
      <input
        type="text"
        className={inputCls}
        placeholder="Fill in the blank"
        value={value ?? ""}
        disabled={disabled}
        onChange={(e) => onChange(e.target.value)}
        autoComplete="off"
        autoCapitalize="off"
        spellCheck={false}
      />
    </div>
  );
}
