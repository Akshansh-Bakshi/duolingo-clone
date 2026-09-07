"use client";

import { useEffect, useState } from "react";
import { api, ApiError } from "@/lib/api";
import type { Profile } from "@/lib/types";
import { LoadingState, ErrorState } from "@/components/common/StateViews";
import styles from "./ProfileView.module.css";

export default function ProfileView() {
  const [profile, setProfile] = useState<Profile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.getProfile();
      setProfile(data);
    } catch (err) {
      setError(err instanceof ApiError ? err.detail : "Failed to load profile.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  if (loading) return <LoadingState label="Loading profile..." />;
  if (error || !profile)
    return <ErrorState message={error ?? "Profile unavailable."} onRetry={load} />;

  const stats = [
    { icon: "⭐", label: "Total XP", value: profile.total_xp },
    { icon: "🔥", label: "Day streak", value: profile.streak },
    { icon: "❤️", label: "Hearts", value: profile.hearts },
    { icon: "💎", label: "Gems", value: profile.gems },
    {
      icon: "👑",
      label: "Skills completed",
      value: `${profile.completed_skills}/${profile.total_skills}`,
    },
    { icon: "📘", label: "Lessons completed", value: profile.lessons_completed },
  ];

  return (
    <div className={styles.page}>
      <div className={`card ${styles.card}`}>
        <div className={styles.avatar} aria-hidden>
          🦉
        </div>
        <div>
          <h1 className={styles.name}>{profile.username}</h1>
          <p className={styles.sub}>Learning Spanish · joined this course</p>
        </div>
      </div>

      <div className={styles.grid}>
        {stats.map((s) => (
          <div key={s.label} className={`card ${styles.statCard}`}>
            <div className={styles.statIcon} aria-hidden>
              {s.icon}
            </div>
            <div className={styles.statValue}>{s.value}</div>
            <div className={styles.statLabel}>{s.label}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
