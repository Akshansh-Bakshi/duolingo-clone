"use client";

import type { ExerciseComponentProps } from "./types";
import styles from "./exercises.module.css";

export default function MultipleChoice({
  exercise,
  value,
  onChange,
  disabled,
  feedback,
}: ExerciseComponentProps) {
  const options = exercise.options ?? [];

  return (
    <div>
      <p className={styles.prompt}>{exercise.question}</p>
      <div className={styles.optionGrid}>
        {options.map((opt) => {
          const isSelected = value === opt;
          let cls = styles.option;
          if (feedback) {
            if (opt === feedback.correctAnswer) cls += ` ${styles.optionCorrect}`;
            else if (isSelected) cls += ` ${styles.optionIncorrect}`;
          } else if (isSelected) {
            cls += ` ${styles.optionSelected}`;
          }
          return (
            <button
              key={opt}
              type="button"
              className={cls}
              disabled={disabled}
              aria-pressed={isSelected}
              onClick={() => onChange(opt)}
            >
              {opt}
            </button>
          );
        })}
      </div>
    </div>
  );
}
