"use client";

import { useUser } from "@/hooks/useUserContext";
import styles from "./TopBar.module.css";

/**
 * Persistent top bar showing the backend-authoritative gamification stats:
 * streak, XP, hearts, and gems. Populated from GET /api/users/me.
 */
export default function TopBar() {
  const { user, loading, error } = useUser();

  return (
    <header className={styles.topbar}>
      <div className={styles.brand}>
        <span className={styles.logoMark} aria-hidden>
          🦉
        </span>
        <span className={styles.brandText}>duolingo</span>
      </div>

      {loading && !user ? (
        <div className={styles.stats} aria-label="Loading stats">
          <div className={styles.skeleton} />
          <div className={styles.skeleton} />
          <div className={styles.skeleton} />
          <div className={styles.skeleton} />
        </div>
      ) : error && !user ? (
        <span style={{ color: "var(--color-red)", fontSize: 13 }}>
          Stats unavailable
        </span>
      ) : user ? (
        <div className={styles.stats}>
          <div className={`${styles.stat} ${styles.streak}`} title="Streak">
            <span className={styles.icon}>🔥</span>
            {user.streak}
          </div>
          <div className={`${styles.stat} ${styles.xp}`} title="Total XP">
            <span className={styles.icon}>⭐</span>
            {user.xp}
          </div>
          <div className={`${styles.stat} ${styles.hearts}`} title="Hearts">
            <span className={styles.icon}>❤️</span>
            {user.hearts}
          </div>
          <div className={`${styles.stat} ${styles.gems}`} title="Gems">
            <span className={styles.icon}>💎</span>
            {user.gems}
          </div>
        </div>
      ) : null}
    </header>
  );
}
