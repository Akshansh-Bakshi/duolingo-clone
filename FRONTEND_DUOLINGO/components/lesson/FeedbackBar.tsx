"use client";

import styles from "./FeedbackBar.module.css";

interface Props {
  correct: boolean;
  correctAnswer: string;
  message: string;
  onContinue: () => void;
}

/** Duolingo's signature bottom feedback bar shown after each submission. */
export default function FeedbackBar({
  correct,
  correctAnswer,
  message,
  onContinue,
}: Props) {
  return (
    <div
      className={`${styles.bar} ${correct ? styles.correct : styles.incorrect}`}
      role="status"
    >
      <div className={styles.inner}>
        <div className={styles.left}>
          <span className={styles.icon} aria-hidden>
            {correct ? "✅" : "❌"}
          </span>
          <div>
            <div
              className={`${styles.title} ${
                correct ? styles.titleCorrect : styles.titleIncorrect
              }`}
            >
              {correct ? "Nicely done!" : "Not quite"}
            </div>
            {!correct && correctAnswer && (
              <div className={styles.answer}>
                Correct answer: <strong>{correctAnswer}</strong>
              </div>
            )}
            {message && (
              <div className={styles.answer} style={{ marginTop: 2 }}>
                {message}
              </div>
            )}
          </div>
        </div>
        <button
          className={`btn ${correct ? "btn-primary" : "btn-red"} ${styles.continueBtn}`}
          onClick={onContinue}
          autoFocus
        >
          Continue
        </button>
      </div>
    </div>
  );
}
