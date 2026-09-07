"use client";

import { useMemo, useState } from "react";
import type { ExerciseComponentProps } from "./types";
import styles from "./exercises.module.css";

function shuffledIndices(n: number): number[] {
  const arr = Array.from({ length: n }, (_, i) => i);
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

/**
 * Match-the-pairs exercise. The backend expects a single canonical string
 * of all pairs joined as "left-right,left-right,..." in the original pair
 * order (FINAL_HANDOFF.md section 9) — built from whatever the learner
 * actually matched, not necessarily the correct pairing.
 */
export default function MatchPairs({
  exercise,
  onChange,
  disabled,
  feedback,
}: ExerciseComponentProps) {
  const pairs = exercise.data?.pairs ?? [];

  // Shuffle the right-hand column once per exercise instance.
  const rightOrder = useMemo(() => shuffledIndices(pairs.length), [exercise.id]);
  const rightItems = rightOrder.map((i) => pairs[i]?.right ?? "");

  const [selectedLeft, setSelectedLeft] = useState<number | null>(null);
  const [matches, setMatches] = useState<Record<number, number>>({}); // leftIdx -> position in rightItems
  const matchedRightPositions = new Set(Object.values(matches));

  const emit = (m: Record<number, number>) => {
    const answer = pairs
      .map((p, leftIdx) => `${p.left}-${rightItems[m[leftIdx]] ?? ""}`)
      .join(",");
    onChange(answer);
  };

  const clickLeft = (idx: number) => {
    if (disabled || matches[idx] !== undefined) return;
    setSelectedLeft((cur) => (cur === idx ? null : idx));
  };

  const clickRight = (position: number) => {
    if (disabled || selectedLeft == null || matchedRightPositions.has(position))
      return;
    const next = { ...matches, [selectedLeft]: position };
    setMatches(next);
    setSelectedLeft(null);
    if (Object.keys(next).length === pairs.length) {
      emit(next);
    }
  };

  return (
    <div>
      <p className={styles.prompt}>{exercise.question}</p>
      <div className={styles.matchGrid}>
        <div className={styles.matchCol}>
          {pairs.map((p, idx) => {
            const isMatched = matches[idx] !== undefined;
            const isSelected = selectedLeft === idx;
            let cls = styles.matchItem;
            if (isMatched) cls += ` ${styles.matchItemMatched}`;
            else if (isSelected) cls += ` ${styles.matchItemSelected}`;
            return (
              <button
                key={idx}
                type="button"
                className={cls}
                disabled={disabled || isMatched}
                onClick={() => clickLeft(idx)}
              >
                {p.left}
              </button>
            );
          })}
        </div>
        <div className={styles.matchCol}>
          {rightItems.map((label, position) => {
            const isMatched = matchedRightPositions.has(position);
            let cls = styles.matchItem;
            if (isMatched) cls += ` ${styles.matchItemMatched}`;
            return (
              <button
                key={position}
                type="button"
                className={cls}
                disabled={disabled || isMatched}
                onClick={() => clickRight(position)}
              >
                {label}
              </button>
            );
          })}
        </div>
      </div>

      {Object.keys(matches).length < pairs.length && (
        <p style={{ marginTop: 16, fontSize: 13, color: "var(--color-text-soft)" }}>
          Tap a word on the left, then its match on the right.
        </p>
      )}
      {feedback && !feedback.correct && (
        <p style={{ marginTop: 16, fontSize: 14, color: "var(--color-text-soft)" }}>
          Correct pairing: <strong>{feedback.correctAnswer}</strong>
        </p>
      )}
    </div>
  );
}
