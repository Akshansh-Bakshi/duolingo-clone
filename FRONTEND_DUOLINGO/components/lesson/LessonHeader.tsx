"use client";

import { useRouter } from "next/navigation";
import styles from "./LessonHeader.module.css";

interface Props {
  current: number; // 1-indexed
  total: number;
  hearts: number;
}

/** Top bar of the lesson player: close/back control, progress bar, hearts. */
export default function LessonHeader({ current, total, hearts }: Props) {
  const router = useRouter();
  const pct = total > 0 ? Math.min(100, (current / total) * 100) : 0;

  return (
    <div className={styles.header}>
      <button
        className={styles.closeBtn}
        aria-label="Exit lesson"
        onClick={() => router.push("/learn")}
      >
        ✕
      </button>
      <div
        className={styles.track}
        role="progressbar"
        aria-valuenow={Math.round(pct)}
        aria-valuemin={0}
        aria-valuemax={100}
      >
        <div className={styles.fill} style={{ width: `${pct}%` }} />
      </div>
      <div className={styles.hearts}>
        <span aria-hidden>❤️</span> {hearts}
      </div>
    </div>
  );
}
