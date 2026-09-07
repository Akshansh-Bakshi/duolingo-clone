"use client";

import type { ExerciseComponentProps } from "./types";
import styles from "./exercises.module.css";

/** Free-text translation exercise, e.g. "Translate: Hello" -> "Hola". */
export default function Translate({
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
