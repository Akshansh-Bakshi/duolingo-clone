"use client";

import { useEffect, useState } from "react";
import { api, ApiError } from "@/lib/api";
import type { Leaderboard } from "@/lib/types";
import { LoadingState, ErrorState, EmptyState } from "@/components/common/StateViews";
import styles from "./LeaderboardView.module.css";

export default function LeaderboardView() {
  const [board, setBoard] = useState<Leaderboard | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.getLeaderboard();
      setBoard(data);
    } catch (err) {
      setError(
        err instanceof ApiError ? err.detail : "Failed to load the leaderboard."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  if (loading) return <LoadingState label="Loading leaderboard..." />;
  if (error) return <ErrorState message={error} onRetry={load} />;
  if (!board || board.entries.length === 0)
    return (
      <EmptyState
        title="No one's on the board yet"
        message="Complete a lesson to earn XP and appear here."
      />
    );

  return (
    <div className={styles.page}>
      <h1 className={styles.title}>Leaderboard</h1>
      <p className={styles.subtitle}>Ranked by total XP</p>

      <div className={styles.list}>
        {board.entries.map((entry) => {
          const isSelf = entry.username === "Learner";
          return (
            <div
              key={entry.rank}
              className={`card ${styles.row} ${isSelf ? styles.rowSelf : ""}`}
            >
              <span
                className={`${styles.rank} ${entry.rank <= 3 ? styles.rankTop : ""}`}
              >
                {entry.rank <= 3 ? ["🥇", "🥈", "🥉"][entry.rank - 1] : entry.rank}
              </span>
              <span className={styles.avatar} aria-hidden>
                {entry.username.charAt(0).toUpperCase()}
              </span>
              <span className={styles.name}>
                {entry.username}
                {isSelf ? " (you)" : ""}
              </span>
              <span className={styles.xp}>{entry.xp} XP</span>
            </div>
          );
        })}
      </div>
    </div>
  );
}
