"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { ApiError } from "@/lib/api";
import styles from "./Modal.module.css";

interface Props {
  onRefill: () => Promise<void>;
}

/** Shown when hearts reach 0, either before starting or mid-lesson.
 * Offers the mocked practice/refill action; blocks further submission
 * until hearts are restored. */
export default function OutOfHearts({ onRefill }: Props) {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleRefill = async () => {
    setLoading(true);
    setError(null);
    try {
      await onRefill();
    } catch (err) {
      setError(err instanceof ApiError ? err.detail : "Couldn't refill hearts.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.overlay}>
      <div className={styles.panel}>
        <div className={styles.emoji} aria-hidden>
          💔
        </div>
        <h2 className={styles.title}>Out of hearts!</h2>
        <p className={styles.subtitle}>
          You've run out of hearts. Practice to refill them and keep going, or
          head back to the path.
        </p>

        {error && (
          <p style={{ color: "var(--color-red)", marginBottom: 16, fontSize: 14 }}>
            {error}
          </p>
        )}

        <div className={styles.actions}>
          <button
            className="btn btn-primary btn-block"
            onClick={handleRefill}
            disabled={loading}
          >
            {loading ? "Refilling..." : "Practice to refill hearts"}
          </button>
          <button
            className="btn btn-outline btn-block"
            onClick={() => router.push("/learn")}
          >
            Back to path
          </button>
        </div>
      </div>
    </div>
  );
}
