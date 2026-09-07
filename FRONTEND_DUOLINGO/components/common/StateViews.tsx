"use client";

import styles from "./StateViews.module.css";

export function LoadingState({ label = "Loading..." }: { label?: string }) {
  return (
    <div className={styles.wrap} role="status" aria-live="polite">
      <div className={styles.spinner} />
      <p className={styles.subtitle}>{label}</p>
    </div>
  );
}

export function ErrorState({
  title = "Something went wrong",
  message,
  onRetry,
}: {
  title?: string;
  message: string;
  onRetry?: () => void;
}) {
  return (
    <div className={styles.wrap} role="alert">
      <div className={styles.emoji}>😵</div>
      <div className={styles.title}>{title}</div>
      <p className={styles.subtitle}>{message}</p>
      {onRetry && (
        <button className="btn btn-primary" onClick={onRetry}>
          Try again
        </button>
      )}
    </div>
  );
}

export function EmptyState({
  emoji = "🦉",
  title,
  message,
}: {
  emoji?: string;
  title: string;
  message?: string;
}) {
  return (
    <div className={styles.wrap}>
      <div className={styles.emoji}>{emoji}</div>
      <div className={styles.title}>{title}</div>
      {message && <p className={styles.subtitle}>{message}</p>}
    </div>
  );
}
