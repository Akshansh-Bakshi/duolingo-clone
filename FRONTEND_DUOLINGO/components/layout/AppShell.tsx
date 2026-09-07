"use client";

import type { ReactNode } from "react";
import { UserProvider } from "@/hooks/useUserContext";
import TopBar from "./TopBar";
import SideNav from "./SideNav";
import styles from "./AppShell.module.css";

/**
 * Shared chrome for every "main" page (learn, profile, leaderboard, settings):
 * top bar with gamification stats + side/bottom navigation.
 * The lesson player intentionally does NOT use this shell — it's a
 * distraction-free full-screen experience, matching Duolingo's lesson UX.
 */
export default function AppShell({ children }: { children: ReactNode }) {
  return (
    <UserProvider>
      <TopBar />
      <div className={styles.wrapper}>
        <SideNav />
        <main className={styles.content}>{children}</main>
      </div>
    </UserProvider>
  );
}
