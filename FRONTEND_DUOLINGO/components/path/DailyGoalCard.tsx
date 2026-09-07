"use client";

import { useUser } from "@/hooks/useUserContext";
import styles from "./DailyGoalCard.module.css";

const RADIUS = 22;
const CIRCUMFERENCE = 2 * Math.PI * RADIUS;

/**
 * Daily XP goal indicator, e.g. "30 / 50 XP". Values come straight from
 * GET /api/users/me (daily_xp, daily_goal) — no client-side computation.
 */
export default function DailyGoalCard() {
  const { user, loading } = useUser();

  if (loading || !user) return null;

  const pct = Math.min(1, user.daily_goal > 0 ? user.daily_xp / user.daily_goal : 0);
  const reached = user.daily_xp >= user.daily_goal && user.daily_goal > 0;
  const offset = CIRCUMFERENCE * (1 - pct);

  return (
    <div className={`card ${styles.card}`}>
      <div className={styles.ringWrap}>
        <svg width="56" height="56" className={styles.ringSvg}>
          <circle
            className={styles.ringTrack}
            cx="28"
            cy="28"
            r={RADIUS}
          />
          <circle
            className={styles.ringProgress}
            cx="28"
            cy="28"
            r={RADIUS}
            strokeDasharray={CIRCUMFERENCE}
            strokeDashoffset={offset}
          />
        </svg>
        <div className={styles.ringIcon} aria-hidden>
          {reached ? "🎉" : "🎯"}
        </div>
      </div>
      <div>
        <div className={styles.title}>Daily Goal</div>
        <div className={styles.sub}>
          {reached ? (
            <span className={styles.reached}>Goal reached! 🎉</span>
          ) : (
            `${user.daily_xp} / ${user.daily_goal} XP`
          )}
        </div>
      </div>
    </div>
  );
}
