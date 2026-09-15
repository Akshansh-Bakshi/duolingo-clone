"use client";

import { useRouter } from "next/navigation";
import type { PathSkill } from "@/lib/types";
import styles from "./SkillNode.module.css";

interface Props {
  skill: PathSkill;
  offset: number; // horizontal stagger for the zig-zag path layout
  isNextUp: boolean; // highlight the first AVAILABLE skill with a "START" badge
}

/**
 * A single node in the skill path. Status (LOCKED / AVAILABLE / COMPLETED)
 * is entirely server-computed — this component only renders it, never
 * evaluates required_skill_id itself.
 */
export default function SkillNode({ skill, offset, isNextUp }: Props) {
  const router = useRouter();

  const handleClick = () => {
    if (skill.status === "LOCKED") return;
    const sortedLessons = [...skill.lessons].sort(
      (a, b) => a.order_index - b.order_index
    );
    if (sortedLessons.length === 0) return;
    // completion_percent (server-computed as completed_count / total * 100)
    // tells us how many lessons in this skill are already done — jump to
    // the next incomplete one instead of always reopening lesson 1.
    const completedCount = Math.round(
      (skill.completion_percent / 100) * sortedLessons.length
    );
    const nextIndex = Math.min(completedCount, sortedLessons.length - 1);
    router.push(`/lesson/${sortedLessons[nextIndex].id}`);
  };

  const statusClass =
    skill.status === "COMPLETED"
      ? styles.completed
      : skill.status === "AVAILABLE"
      ? styles.available
      : styles.locked;

  const icon =
    skill.status === "LOCKED"
      ? "🔒"
      : skill.status === "COMPLETED"
      ? "👑"
      : "⭐";

  return (
    <div
      className={styles.col}
      style={{ transform: `translateX(${offset}px)` }}
    >
      {isNextUp && <div className={styles.startBadge}>Start</div>}
      <button
        className={`${styles.nodeBtn} ${statusClass}`}
        onClick={handleClick}
        disabled={skill.status === "LOCKED"}
        aria-label={`${skill.title} — ${skill.status.toLowerCase()}`}
        title={skill.title}
      >
        <span className={skill.status === "LOCKED" ? styles.lockIcon : ""}>
          {icon}
        </span>
      </button>
      <div
        className={`${styles.label} ${
          skill.status === "LOCKED" ? styles.lockedLabel : ""
        }`}
      >
        {skill.title}
      </div>
      <div className={styles.crownRow} aria-hidden>
        {Array.from({ length: 5 }).map((_, i) => (
          <span
            key={i}
            className={`${styles.crownIcon} ${
              i < skill.crowns ? styles.crownFilled : ""
            }`}
          >
            👑
          </span>
        ))}
      </div>
    </div>
  );
}