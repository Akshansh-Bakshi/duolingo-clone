"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import styles from "./SideNav.module.css";

const LINKS = [
  { href: "/learn", label: "Learn", icon: "🏠" },
  { href: "/leaderboard", label: "Leaderboard", icon: "🏆" },
  { href: "/profile", label: "Profile", icon: "👤" },
  { href: "/settings", label: "Settings", icon: "⚙️" },
];

export default function SideNav() {
  const pathname = usePathname();

  return (
    <>
      <nav className={styles.nav} aria-label="Primary">
        {LINKS.map((link) => {
          const active = pathname?.startsWith(link.href);
          return (
            <Link
              key={link.href}
              href={link.href}
              className={`${styles.link} ${active ? styles.linkActive : ""}`}
            >
              <span className={styles.icon} aria-hidden>
                {link.icon}
              </span>
              {link.label}
            </Link>
          );
        })}
      </nav>

      <nav className={styles.mobileNav} aria-label="Primary">
        {LINKS.map((link) => {
          const active = pathname?.startsWith(link.href);
          return (
            <Link
              key={link.href}
              href={link.href}
              className={`${styles.mobileLink} ${
                active ? styles.mobileLinkActive : ""
              }`}
            >
              <span className={styles.mobileIcon} aria-hidden>
                {link.icon}
              </span>
              {link.label}
            </Link>
          );
        })}
      </nav>
    </>
  );
}
