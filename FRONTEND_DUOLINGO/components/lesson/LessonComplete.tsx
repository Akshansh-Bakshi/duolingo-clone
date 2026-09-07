"use client";

import { useRouter } from "next/navigation";
import type { CompleteResponse } from "@/lib/types";
import styles from "./Modal.module.css";

interface Props {
  result: CompleteResponse;
}

/** Lesson-complete celebration modal. Every number shown comes directly
 * from the /complete response — nothing is recomputed client-side. */
export default function LessonComplete({ result }: Props) {
  const router = useRouter();

  return (
    <div className={styles.overlay}>
      <div className={styles.panel}>
        <div className={styles.emoji} aria-hidden>
          {result.perfect ? "🏆" : "🎉"}
        </div>
        <h2 className={styles.title}>
          {result.perfect ? "Perfect lesson!" : "Lesson complete!"}
        </h2>
        <p className={styles.subtitle}>
          {result.perfect
            ? "You got every exercise right."
            : "Great effort — keep practicing to master this skill."}
        </p>

        <div className={styles.statGrid}>
          <div className={`${styles.statCard} ${styles.xpStat}`}>
            <div className={styles.statValue}>+{result.xp_earned} XP</div>
            <div className={styles.statLabel}>Earned</div>
          </div>
          <div className={`${styles.statCard} ${styles.streakStat}`}>
            <div className={styles.statValue}>{result.streak}</div>
            <div className={styles.statLabel}>Day streak</div>
          </div>
          <div className={`${styles.statCard} ${styles.crownStat}`}>
            <div className={styles.statValue}>{result.skill_crowns} 👑</div>
            <div className={styles.statLabel}>Skill crowns</div>
          </div>
          <div className={`${styles.statCard} ${styles.heartStat}`}>
            <div className={styles.statValue}>{result.hearts_remaining} ❤️</div>
            <div className={styles.statLabel}>Hearts left</div>
          </div>
        </div>

        {result.daily_goal_reached && (
          <div className={styles.goalBanner}>
            🎯 Daily goal reached — {result.daily_xp}/{result.daily_goal} XP!
          </div>
        )}

        <div className={styles.actions}>
          <button
            className="btn btn-primary btn-block"
            onClick={() => router.push("/learn")}
          >
            Continue
          </button>
        </div>
      </div>
    </div>
  );
}
