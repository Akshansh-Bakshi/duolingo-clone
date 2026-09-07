"use client";

// Global gamification state (streak / XP / hearts / gems / daily goal).
// Backed entirely by GET /api/users/me. Components never invent or locally
// mutate these values — they call refresh() after any action that could
// change them server-side (submit, complete, practice/refill).

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";
import { api, ApiError } from "@/lib/api";
import type { User } from "@/lib/types";

interface UserContextValue {
  user: User | null;
  loading: boolean;
  error: string | null;
  refresh: () => Promise<void>;
  /** Optimistically merge partial fields (e.g. hearts_remaining from a
   * submit/complete response) so the top bar updates instantly without
   * waiting on a full refetch. Always safe because the values still
   * originate from a backend response, never invented client-side. */
  applyPartial: (patch: Partial<User>) => void;
}

const UserContext = createContext<UserContextValue | undefined>(undefined);

export function UserProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    try {
      setError(null);
      const data = await api.getMe();
      setUser(data);
    } catch (err) {
      setError(err instanceof ApiError ? err.detail : "Failed to load user.");
    } finally {
      setLoading(false);
    }
  }, []);

  const applyPartial = useCallback((patch: Partial<User>) => {
    setUser((prev) => (prev ? { ...prev, ...patch } : prev));
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  return (
    <UserContext.Provider
      value={{ user, loading, error, refresh, applyPartial }}
    >
      {children}
    </UserContext.Provider>
  );
}

export function useUser() {
  const ctx = useContext(UserContext);
  if (!ctx) throw new Error("useUser must be used within a UserProvider");
  return ctx;
}
