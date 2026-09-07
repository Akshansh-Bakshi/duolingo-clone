"use client";

import type { ExerciseComponentProps } from "./types";
import styles from "./exercises.module.css";

/** Free-typed answer exercise — functionally identical UI to Translate,
 * kept as a separate component per the required architecture since the
 * two exercise types are semantically distinct in the API contract. */
export default function TypeAnswer({
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
        placeholder="Type your answer"
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
