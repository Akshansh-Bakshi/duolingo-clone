import styles from "./page.module.css";

export default function SettingsPage() {
  return (
    <div className={styles.page}>
      <h1 style={{ marginBottom: 20 }}>Settings</h1>
      <div className={`card ${styles.card}`}>
        <div className={styles.emoji} aria-hidden>
          🚧
        </div>
        <h2 style={{ fontSize: 18, marginBottom: 8 }}>Coming soon</h2>
        <p style={{ color: "var(--color-text-soft)", fontSize: 14, marginBottom: 24 }}>
          Account, notification, and language settings aren&apos;t part of this
          assignment&apos;s scope — this is a placeholder screen.
        </p>
        <div className={styles.row}>
          <span className={styles.label}>Learner</span>
          <span>Learner</span>
        </div>
        <div className={styles.row}>
          <span className={styles.label}>Course</span>
          <span>Spanish for English Speakers</span>
        </div>
        <div className={styles.row}>
          <span className={styles.label}>Sound effects</span>
          <span>On</span>
        </div>
      </div>
    </div>
  );
}
