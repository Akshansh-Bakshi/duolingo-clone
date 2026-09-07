// Thin API access layer. Every function here maps 1:1 to an endpoint documented
// in FRONTEND_API_CONTRACT.md. Components should never call fetch() directly —
// they go through this module so the base URL and error handling live in one place.

import type {
  Course,
  CoursePath,
  CompleteRequest,
  CompleteResponse,
  Leaderboard,
  Lesson,
  PracticeResponse,
  Profile,
  Progress,
  SubmitRequest,
  SubmitResponse,
  User,
} from "./types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL?.replace(/\/$/, "") ||
  "http://127.0.0.1:8000";

/**
 * ApiError carries the HTTP status and, when available, the backend's
 * `detail` message so the UI can distinguish 404 / 409 / 400 / 500 and
 * show a targeted message instead of a generic failure toast.
 */
export class ApiError extends Error {
  status: number;
  detail: string;

  constructor(status: number, detail: string) {
    super(detail);
    this.name = "ApiError";
    this.status = status;
    this.detail = detail;
  }
}

async function request<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
      cache: "no-store",
    });
  } catch (err) {
    // Network-level failure: backend unreachable, CORS, DNS, offline, etc.
    throw new ApiError(
      0,
      "Could not reach the server. Check that the backend is running and reachable."
    );
  }

  if (!response.ok) {
    let detail = response.statusText || "Request failed";
    try {
      const body = await response.json();
      if (body?.detail) detail = body.detail;
    } catch {
      // response had no JSON body — fall back to statusText
    }
    throw new ApiError(response.status, detail);
  }

  // Some endpoints could theoretically return empty bodies; guard for that.
  const text = await response.text();
  return (text ? JSON.parse(text) : undefined) as T;
}

export const api = {
  health: () => request<{ status: string }>("/health"),

  getMe: () => request<User>("/api/users/me"),

  getCourses: () => request<Course[]>("/api/courses"),

  getCoursePath: (courseId: number) =>
    request<CoursePath>(`/api/courses/${courseId}/path`),

  getLesson: (lessonId: number) =>
    request<Lesson>(`/api/lessons/${lessonId}`),

  submitAnswer: (lessonId: number, body: SubmitRequest) =>
    request<SubmitResponse>(`/api/lessons/${lessonId}/submit`, {
      method: "POST",
      body: JSON.stringify(body),
    }),

  completeLesson: (lessonId: number, body: CompleteRequest) =>
    request<CompleteResponse>(`/api/lessons/${lessonId}/complete`, {
      method: "POST",
      body: JSON.stringify(body),
    }),

  getProgress: () => request<Progress>("/api/progress"),

  practiceRefill: () =>
    request<PracticeResponse>("/api/progress/practice", { method: "POST" }),

  getProfile: () => request<Profile>("/api/profile"),

  getLeaderboard: () => request<Leaderboard>("/api/leaderboard"),
};

export { API_BASE_URL };
