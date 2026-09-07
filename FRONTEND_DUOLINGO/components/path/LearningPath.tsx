"use client";

import { useEffect, useState } from "react";
import { api, ApiError } from "@/lib/api";
import type { CoursePath, PathSkill } from "@/lib/types";
import { LoadingState, ErrorState, EmptyState } from "@/components/common/StateViews";
import UnitSection from "./UnitSection";
import DailyGoalCard from "./DailyGoalCard";
import styles from "./LearningPath.module.css";

type LoadState =
  | { status: "loading" }
  | { status: "error"; message: string }
  | { status: "ready"; path: CoursePath };

export default function LearningPath() {
  const [state, setState] = useState<LoadState>({ status: "loading" });

  const load = async () => {
    setState({ status: "loading" });
    try {
      const courses = await api.getCourses();
      if (courses.length === 0) {
        setState({
          status: "error",
          message: "No course is available yet. Run the backend seed script.",
        });
        return;
      }
      const path = await api.getCoursePath(courses[0].id);
      setState({ status: "ready", path });
    } catch (err) {
      setState({
        status: "error",
        message:
          err instanceof ApiError
            ? err.detail
            : "Failed to load the learning path.",
      });
    }
  };

  useEffect(() => {
    load();
  }, []);

  if (state.status === "loading") {
    return <LoadingState label="Loading your learning path..." />;
  }

  if (state.status === "error") {
    return <ErrorState message={state.message} onRetry={load} />;
  }

  const { path } = state;
  const sortedUnits = [...path.units].sort(
    (a, b) => a.order_index - b.order_index
  );

  if (sortedUnits.length === 0) {
    return (
      <EmptyState
        title="No content yet"
        message="This course doesn't have any units yet."
      />
    );
  }

  // Find the first AVAILABLE skill across the whole course, in order,
  // purely to render a "Start" badge — a UI hint only, not a source of truth.
  const allSkillsInOrder: PathSkill[] = sortedUnits.flatMap((u) =>
    [...u.skills].sort((a, b) => a.order_index - b.order_index)
  );
  const nextUp = allSkillsInOrder.find((s) => s.status === "AVAILABLE");

  let runningOffset = 0;

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <h1 className={styles.courseTitle}>{path.course_name}</h1>
      </header>

      <DailyGoalCard />

      <div style={{ marginTop: 28 }}>
        {sortedUnits.map((unit) => {
          const el = (
            <UnitSection
              key={unit.id}
              unit={unit}
              startIndexOffset={runningOffset}
              nextUpSkillId={nextUp?.id ?? null}
            />
          );
          runningOffset += unit.skills.length;
          return el;
        })}
      </div>
    </div>
  );
}
